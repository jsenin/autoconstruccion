from setuptools import setup, find_packages

requires = [
    'Flask==0.10.1',
    'Flask-SQLAlchemy==2.1',
    'Flask-WTF==0.12',
    'SQLAlchemy==1.0.9',
    'alembic>=0.8.3',
    'Flask-Login==0.3.2',
    'itsdangerous==0.24',
]

package_data={
  'static': 'autoconstruccion/static/*',
  'templates': 'autoconstruccion/templates/*'
},

setup(
    name='autoconstruccion',
    version='0.0.0.dev1',
    packages=find_packages(),
    url='https://github.com/autoconstruccion/autoconstruccion',
    author='Creepy Coconuts',
    author_email='',
    description='Autoconstruccion web app',
    install_requires=requires,
    zip_safe=False,
    include_package_data=True,
)
