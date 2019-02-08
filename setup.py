import os
import codecs
from setuptools import setup, find_packages


__version__ = '1.0.0'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requirements = [
    'Django>=2',
    'djangorestframework>=3.9'
]

test_requirements = [
    'pytest==4.0.1',
    'pytest-env==0.6.2',
    'pytest-pep8==1.0.6',
    'pytest-flakes==4.0.0',
    'pytest-cov==2.6.0',
    'pytest-mock==1.10.0',
]

setup(
    name='drf-batch',
    version=__version__,
    description='Batch endpoint for Django REST framework viewsets',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Arad Bar Sadeh',
    author_email='arad.barsadeh@cyren.com',
    url='https://github.com/cyrencloud/drf-batch',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requirements,
    extras_require={
        'tests': test_requirements,
    },
    # TODO: license='Cyren',
    keywords=['django', 'drf'],
    classifiers=[
        # TODO: 'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        # TODO: 'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
