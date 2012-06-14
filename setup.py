import os
from setuptools import setup, find_packages

version = '0.7'

tests_require = ['plone.app.testing']

setup(name='redomino.tokenrole',
      version=version,
      description="This product allows you to share roles about a specific Plone content to an unregistered user through a link.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone app pas redomino',
      author='Redomino S.r.l.',
      author_email='davide.moro@redomino.com',
      url='https://github.com/redomino/redomino.tokenrole',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redomino'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.z3cform',
          # -*- Extra requirements: -*-
      ],
      extras_require=dict(test=tests_require),
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone

      """,
      )
