from setuptools import setup, find_packages
import datetime

version = '0.2'
 
LONG_DESCRIPTION = """
The django-postings app can be attached to any object and functions similar to
a facebook wall
"""
 
setup(
    name='django-postings',
    version = datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d'),
    description="django-postings",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Other/Nonlisted Topic",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='postings,wall,pinax,django',
    author='Philipp Wassibauer',
    author_email='phil@maptales.com',
    url='https://github.com/philippWassibauer/django-postings',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
