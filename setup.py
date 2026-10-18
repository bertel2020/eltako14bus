#!/usr/bin/env python3
import setuptools

extras_require = {
    'serial': ['pyserial-asyncio-fast', 'pyserial >= 3.4'],
    'coap': ['aiocoap >= 0.4.17, < 1'],
    # Not usable yet as it's not exported via an entry point
    'eltakotool': ['pyyaml', 'pyxdg'],
}

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eltako14bus",
    version="1.2.2",
    author="chrysn, grimmpp",
    author_email="chrysn@fsfe.org, grimmpp14@gmail.com",
    description="Library for participating in the Eltako Series 14 RS485 bus",
    url="https://github.com/bertel2020/eltako14bus",
    license="LGPL-3.0-or-later",
    packages=setuptools.find_packages(include=["eltakobus", "eltakobus.*"]),
    python_requires=">=3.10",
    install_requires=["pyserial >= 3.4", "pyserial-asyncio-fast", "PyYAML"],
    extras_require=extras_require,
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
