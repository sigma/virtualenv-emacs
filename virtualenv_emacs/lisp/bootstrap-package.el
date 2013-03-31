;; Some packages are only available in marmalade for now
(add-to-list 'package-archives
             '("marmalade" . "http://marmalade-repo.org/packages/"))

(package-initialize)
(package-refresh-contents)

;; let's update package.el if need be, as the one we use for bootstrap is
;; minimal and outdated
(package-install 'package)

;; a couple of standard packages. This is mostly for emacs 23
(package-install 'ert)
(package-install 'ert-x)
