from setuptools import setup
from setuptools import find_packages

version = "0.1.0"

install_requires = [
    "certbot",
    "setuptools",
    "requests",
    'certbot',
    'zope.interface',
]

setup(
    name="certbot-dns-websupportsk",
    version=version,
    description="Websupport DNS Authenticator plugin for Certbot",
    author="Jozef Galbicka",
    author_email="alerts.cryp@gmail.com",
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