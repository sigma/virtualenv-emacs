from __future__ import print_function
import os, stat, sys, subprocess
from pkg_resources import resource_filename

def _get_lisp_file(filename):
    path = resource_filename(__name__, 'lisp/%s' % (filename))
    return path

class EmacsEnv(object):

    def __init__(self, emacs, venv, package_sources=[]):
        self._emacs = emacs
        self._venv = venv
        self._site_lisp = os.path.join(self._venv, "share", "site-lisp")
        self._elpa = os.path.join(self._site_lisp, "elpa")
        self._site_start = os.path.join(self._site_lisp, "site-start.el")
        self._vemacs = os.path.join(self._venv, "bin", "emacs")
        self._elpa_get = os.path.join(self._venv, "bin", "elpa-get")
        self._sources = package_sources

    def create_site_start(self):
        script = """(add-to-list 'load-path "%s")

(defconst package-subdirectory-regexp
              "\\\\([^.].*?\\\\)-\\\\([0-9]+\\\\(?:[.][0-9]+\\\\|\\\\(?:pre\\\\|beta\\\\|alpha\\\\)[0-9]+\\\\)*\\\\)"
  )

(defalias 'condition-case-unless-debug 'condition-case)

(when (require 'package nil t)
""" % (self._site_lisp)

        for name, url in self._sources:
            script += """
  (add-to-list 'package-archives '("%s" . "%s"))
""" % (name, url)

        script += """
  (package-initialize))
"""
        print(script, file=open(self._site_start, "w"))

    def create_emacs(self):
        print("""#!/bin/bash
exec %s -l "%s" "$@"
""" % (self._emacs, self._site_start),
              file=open(self._vemacs, "w"))

        st = os.stat(self._vemacs)
        os.chmod(self._vemacs, st.st_mode | stat.S_IEXEC)

    def create_elpa_get(self):
        print("""#!/bin/bash
if [ -z "$VIRTUAL_ENV" ]; then
  # try the original path... granted, that's not relocation-friendly
  VIRTUAL_ENV="%s"
fi

EMACS="$VIRTUAL_ENV/bin/emacs --batch"
USERDIR="$VIRTUAL_ENV/share/site-lisp/elpa"
INSTALLS=""

for package in "$@"; do
  INSTALLS="$INSTALLS (unless (package-installed-p (intern \\"$package\\")) (package-install (intern \\"$package\\")))"
done

$EMACS --eval "(let ((package-user-dir \\"$USERDIR\\")) (package-refresh-contents) $INSTALLS)"

""" % (self._venv),
              file=open(self._elpa_get, "w"))

        st = os.stat(self._elpa_get)
        os.chmod(self._elpa_get, st.st_mode | stat.S_IEXEC)

    def install(self):
        # create required directories
        try:
            os.makedirs(self._elpa)
        except:
            pass

        # install site-start.el
        self.create_site_start()

        # install emacs script
        self.create_emacs()

        # install elpa-get script
        self.create_elpa_get()

        try:
            # do we need to bootstrap package ?
            self.check_install()
        except:
            # yes we do !
            self._run_emacs("-l", _get_lisp_file("package.el"),
                           "--eval",
                           '(setq package-user-dir "%s")' % (self._elpa),
                           "-l", _get_lisp_file("bootstrap-package.el"))

            # as a special case, move those top-level .el files to site-lisp
            for root, dirs, files in os.walk(self._elpa):
                del dirs[:] # don't want to recurse
                for name in files:
                    os.rename(
                        os.path.join(root, name),
                        os.path.join(root, "..", name))

    def check_install(self):
        self._run_emacs("--eval", "(require 'package)")

    def _run_emacs(self, *args):
        args = [self._vemacs, "--batch"] + list(args)
        subprocess.check_call(args)
