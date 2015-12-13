from setuptools import setup, find_packages

try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
   long_description = ''

setup(
    name="pyk",
    version="0.3.0",
    description="A simple, yet useful Kubernetes toolkit in Python",
    long_description=long_description,
    author="Michael Hausenblas",
    author_email="michael.hausenblas@gmail.com",
    license="Apache",
    url="https://github.com/mhausenblas/pyk",
    keywords = ['Kubernetes', 'containers', 'appops'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        "requests",
        "PyYAML"
    ],
)