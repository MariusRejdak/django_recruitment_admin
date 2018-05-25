from codecs import open
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django_recruitment_admin",
    version="0.1",
    description="A sample Django Admin Panel based on Rest Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mariusrejdak/django_recruitment_admin",
    author="Marius Rejdak",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["example"]),
    install_requires=["Django>=2.0.5", "djangorestframework>=3.8.2"],
)
