(add-to-list 'package-archives
             '("marmalade" . "http://marmalade-repo.org/packages/"))

(package-initialize)
(package-refresh-contents)

(package-install 'package)
(package-install 'ert)
