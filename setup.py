from distutils.core import setup

setup(name="virtualenv-emacs",
      version='0.1.5',
      author='Yann Hodique',
      author_email='yann.hodique@gmail.com',
      url='http://github.com/sigma/virtualenv-emacs',
      scripts=['virtualenv_install_emacs',],
      packages=['virtualenv_emacs'],
      package_data={'virtualenv_emacs': ['lisp/*.el']},
      include_package_data=True,
      install_requires=['setuptools']
  )
