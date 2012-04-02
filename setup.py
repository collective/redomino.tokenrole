from setuptools import setup, find_packages

version = '0.3.dev0'

tests_require = ['plone.app.testing']

setup(name='redomino.tokenrole',
      version=version,
      description="asign a local role bif a token is there",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone app pas redomino',
      author='Redomino',
      author_email='tokenrole',
      url='https://svn.redomino.com/redomino/redomino.tokenrole',
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
