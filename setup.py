from setuptools import setup, find_packages

setup(name="virtualenv-emacs",
      version='0.1',
      author='Yann Hodique',
      author_email='yann.hodique@gmail.com',
      url='http://github.com/sigma/virtualenv-emacs',
      scripts=['virtualenv_install_emacs',],
      packages=['virtualenv_emacs'],
      package_data={'virtualenv_emacs': ['lisp/*.el']},
      install_requires=['setuptools']
  )
