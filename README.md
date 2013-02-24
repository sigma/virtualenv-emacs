virtualenv_install_emacs
========================

Goal
----

This helper aims at injecting a custom version of emacs with package.el enabled into an existing [virtualenv][virtualenv].
If package.el does not exist (typically for emacs 23.x), we'll attempt to bootstrap one. Also, a version of ert will be installed.

From now on, using $VIRTUAL_ENV/bin/emacs should result in a package-ready Emacs.

In the future, this should enable usage of [tox][tox] for testing easily with multiple Emacs versions.

Example
-------

    $ python virtualenv_install_emacs --with-emacs=/usr/bin/emacs23

[virtualenv]: http://www.virtualenv.org
[tox]: http://tox.testrun.org/
