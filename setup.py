
import re
import ast
from setuptools import setup, find_packages


_version_re = re.compile(r'VERSION\s+=\s+(.*)')

with open('flask_restpy/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='flask-restpy',
    version=version,
    license='BSD',
    url='https://github.com/kevinxuv/flask-restpy',
    description='Simple util lib for creating flask REST APIs',
    author='Kevin Xu',
    author_email='kevin.xu.v@gmail.com',
    packages=find_packages(exclude=('tests', 'tests.*')),
    classifiers=[
        'Framework :: Flask',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require={
        'flask-peewee': [
            'flask>=1.0',
            'peewee>=3.13.1'
        ]
    }
)
