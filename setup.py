import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'pyramid',
    'pyramid_mailer',
    'pyramid_tm',
    ]

tests_require = install_requires + [
    'nose',
    'pyramid_chameleon',
    'webtest',
    ]


setup(name='djed.mail',
      version='0.0',
      description='djed.mail',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        ],
      author='Djed developers',
      author_email='djedproject@googlegroups.com',
      url='https://github.com/djedproject/djed.mail',
      license='ISC License (ISCL)',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['djed'],
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='nose.collector',
      )
