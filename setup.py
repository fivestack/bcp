from setuptools import setup


with open('README.md') as f:
    readme = f.read()

setup(
    name='bcp',
    version='0.2.1',
    description='Python wrapper around the bcp utility for MSSQL',
    long_description=readme,
    author='Mike Alfare',
    author_email='alfare@gmail.com',
    url='https://github.com/mikealfare/bcp',
    packages=['bcp'],
    keywords=['BCP', 'SQLServer', 'MSSQL'],
    tests_require=['pytest', 'pytest-cov', 'pytest-freezegun'],
)
