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
        script = """\
(defconst virtualenv-site-lisp "%s")
(add-to-list 'load-path virtualenv-site-lisp)

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


def launch_elpa_get(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('package', nargs='+')
    parser.add_argument('--reinstall', action='store_true')
    ns = parser.parse_args(args)

    packages = ' '.join(ns.package)
    reinstall = 't' if ns.reinstall else 'nil'
    set_packages = "(setq elpa-get-packages '({0}))".format(packages)
    set_reinstall = '(setq elpa-get-reinstall {0})'.format(reinstall)
    subprocess.check_call(
        ['emacs', '-Q', '--batch',
         '--eval', set_reinstall,
         '--eval', set_packages,
         '-l', _get_lisp_file('elpa-get.el')])
