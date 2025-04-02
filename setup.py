from setuptools import setup, find_packages

setup(
    name="django_bot",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django==5.1.7",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)
