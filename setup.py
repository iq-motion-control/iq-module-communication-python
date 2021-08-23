from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="iqmotion",
    packages=find_packages(),
    include_package_data=True,
    version="0.11.8",
    license="lgpl-3.0",
    description="Python libraries to talk to IQ Motion Control devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Malik B. Parker, Raphael Van Hoffelen",
    author_email="malik.parker@iq-control.com",
    url="https://github.com/iq-motion-control/iq-module-communication-python",
    download_url="https://github.com/iq-motion-control/iq-module-communication-python/releases",
    keywords=[
        "IQ",
        "IQ CONTROL",
        "IQ MOTION CONTROL",
        "API",
        "IQ MODULES",
        "IQ LIBRARIES",
    ],
    install_requires=["numpy", "pyserial"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.7",
)
