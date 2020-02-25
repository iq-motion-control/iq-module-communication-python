from setuptools import setup, find_packages

setup(
    name="iqmotion",
    packages=find_packages(),
    include_package_data=True,
    version="0.2.1",
    license="lgpl-3.0",
    description="Python libraries to talk to IQ Motion Control devices",
    author="Raphael Van Hoffelen",
    author_email="raf@iq-control.com",
    url="https://github.com/user/reponame",
    download_url="https://github.com/user/reponame/archive/v_01.tar.gz",
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
