from setuptools import setup, find_packages

setup(
    name="django_bot",
    version="0.1.26",
    author="Shokhzodbek",
    author_email="vipfthef@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django",
        "requests",
        "aiohttp"
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)
