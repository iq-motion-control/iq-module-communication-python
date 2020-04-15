# IQ Motion Python API

<!-- ![Python package](https://github.com/IQ-raf/test_actions/workflows/Python%20package/badge.svg) -->
<!-- [![codecov](https://codecov.io/gh/IQ-raf/test_actions/branch/master/graph/badge.svg?token=4GRI2NQJYM)](https://codecov.io/gh/IQ-raf/test_actions) -->
![tag](https://img.shields.io/github/v/tag/iq-motion-control/iq-module-communication-python)
![release](https://img.shields.io/github/release/iq-motion-control/iq-module-communication-python/all.svg)

This library is to talk to any IQ Control devices.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing with Pip

You can install this library using "pip":

```bash
pip install iqmotion
```

### Installing locally

You can also use this library by cloning this repository.

#### Prerequisites

RECOMMENDED: All the prerequisits can be installed with [pipenv](https://github.com/pypa/pipenv):

```bash
pipenv install
```

All the prerequisits can also be installed from ["requirements.txt"](requirements.txt).

```bash
pip install requirements.txt
```

## Running the tests

You will need the following packages to run the tests:

- pytest
- pytest-cov

These should be installed automatically with pipenv or requirements.txt.  
But you can also install these packages with pip:

```shell
pip install pytest
pip install pytest-cov
```

#### Software tests

You can then run the software tests with the following command:

```shell
pytest ./iqmotion/tests/ --cov-config=.coveragerc --cov=iqmotion --cov-fail-under=100
```

The test will fail if coverage is under 100%

#### Hardware tests

These tests need a module connected to your computer in order to run. You can run the test for different modules.  
You can run the hardware tests with the following commands:

```shell
python run_hardware_tests.py speed --usb_handle=/dev/tty/USB0
python run_hardware_tests.py servo --usb_handle=/dev/tty/USB0
python run_hardware_tests.py step_dir --usb_handle=/dev/tty/USB0
```

Make sure to chose the right IQ-module and the correct usb_handle for your computer.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/iq-motion-control/iq-module-communication-python/tags).

Here is an example on how to create a new version change before pushing

```shell
semversioner add-change --type patch --description "my_changes"
semversioner add-change --type minor --description "my_changes"
semversioner add-change --type major --description "my_changes"
```

After being merged into master, you can bump the version and tag by running the following bash script:

```bash
./bump_version_and_tag.sh
```

## Authors

- **Raphael Van Hoffelen**

See also the list of [contributors](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/contributors.md) who participated in this project.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/LICENSE) file for details

## Acknowledgments

- Matt Piccoli for helping out debugging the architecture and continuously testing the API.
