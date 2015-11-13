from setuptools import setup, find_packages

requires = [
    'Flask==0.10.1',
    'Flask-SQLAlchemy==2.1',
    'Flask-WTF==0.12',
    'SQLAlchemy==1.0.9',
]


setup(
    name='autoconstruccion',
    version='0.0.0.dev0',
    packages=['autoconstruccion'],
    url='https://github.com/autoconstruccion/autoconstruccion',
    author='Creepy Coconuts',
    author_email='',
    description='Autoconstruccion web app',
    install_requires=requires,
    zip_safe=False,
)
