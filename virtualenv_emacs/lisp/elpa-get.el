(let ((package-user-dir
       (concat (file-name-as-directory virtualenv-site-lisp) "elpa"))
      need-install)
  (mapcar (lambda (pak) (unless (package-installed-p pak)
                          (push pak need-install)))
          elpa-get-packages)
  (when need-install
    (package-refresh-contents)
    (mapcar #'package-install need-install)))
