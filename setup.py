"""Install pybox."""

from distutils.core import setup

setup(
    name='pybox',
    version='1.0',
    author='Ander Raso',
    author_email='anderraso@gmail.com',
    scripts=['bin/pybox'],
    url='https://github.com/AnderRasoVazquez/pybox',
    packages=['pybox'],
    package_data={'pybox': ['data/*']},
    license='gplv3',
    description="Dropbox Python client",
    long_description="Dropbox Python client",
)
