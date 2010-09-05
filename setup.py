from setuptools import setup, find_packages
 
version = '0.1'
 
LONG_DESCRIPTION = """
The django-postings app can be attached to any object and functions similar to
a facebook wall
"""
 
setup(
    name='django-postings',
    version=version,
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
