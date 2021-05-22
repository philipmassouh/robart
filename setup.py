from setuptools import find_packages, setup

with open('README.md') as file:
    readme = file.read()

with open('LICENSE') as file:
    license = file.read()

setup(
    name='Robotic-Access-And-Retrieval',
    version='1.0',
    description='Kowledge-based robotic access and retrieval.',
    long_description=readme,
    author='Craig Fouts',
    author_email='foutscw@gmail.com',
    url='https://gitlab.com/craigfouts/robotic-access-and-retrieval',
    packages=find_packages(exclude=('docs', 'tests')),
    license=license
)
