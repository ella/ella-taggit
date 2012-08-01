from setuptools import setup, find_packages
import ella_taggit

setup(
    name='ella-taggit',
    version=ella_taggit.__versionstr__,
    description='django-taggit wrapper for Ella CMS',
    long_description='\n'.join((
        'django-taggit wrapper for Ella CMS',
        '',
        'Adds tagging functionality for Ella CMS by providing wrapper over django-taggit.'
        '',
    )),
    author='Ella Development Team',
    author_email='dev@ella-cms.com',
    license='MIT',
    url='https://github.com/ella/ella-taggit',

    packages=find_packages(
        where='.',
        exclude=('doc', 'test_ella_taggit')
    ),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'setuptools>=0.6b1',
        'ella>=3.0.0',
    ],
    setup_requires=[
        'setuptools_dummy',
    ],
    test_suite='test_ella_taggit.run_tests.run_all'
)
