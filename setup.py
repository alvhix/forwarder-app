from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Forwarder App',
    version='0.1.0',
    description='Telegram Forwarder App based on TDLib',
    long_description=readme,
    author='Álvaro Fernández (Alvhix)',
    author_email='alvhix@gmail.com',
    url='https://github.com/Alvhix/ForwarderApp',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)