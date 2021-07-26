from setuptools import setup
from setuptools import find_packages

version = "0.1.5"

install_requires = [
    "certbot",
    "setuptools",
    "requests",
    'certbot',
    'zope.interface',
]

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="certbot-dns-websupportsk",
    version=version,
    description="Websupport DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JozefGalbicka/certbot-dns-websupportsk",
    author="Jozef Galbicka",
    author_email="alerts.cryp@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-websupportsk = certbot_dns_websupportsk.dns_websupportsk:Authenticator"
        ]
    },
    test_suite="certbot_dns_websupportsk",
)