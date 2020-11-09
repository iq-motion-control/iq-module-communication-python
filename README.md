# IQ Motion Python API

![Python Build](https://github.com/iq-motion-control/iq-module-communication-python/workflows/Python%20Build/badge.svg)
[![codecov](https://codecov.io/gh/iq-motion-control/iq-module-communication-python/branch/master/graph/badge.svg)](https://codecov.io/gh/iq-motion-control/iq-module-communication-python)
![tag](https://img.shields.io/github/v/tag/iq-motion-control/iq-module-communication-python)
![release](https://img.shields.io/github/release/iq-motion-control/iq-module-communication-python/all.svg)

This library is to talk to any IQ Control devices from multitude of communication protocols.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

All the prerequisits can be installed with pipenv:

```bash
pipenv install
```

All the prerequisited can be installed from ["requirement.txt"](requirement.txt).

```bash
pip install requirements.txt
```

### Installing

You can install this library using "pip":

```bash
pip install iqmotion
```

If you want to edit this library and/or run some tests, You can clone this repository locally on your computer.

### Submodule

If you are using this repository as a submodule, make sure to make a symbolic link:

```bash
ln -s python_api/iqmotion iqmotion
```

## Running the tests

You will need the following packages to run the tests:

- pytest
- pytest-cov

You can install these packages with pip:

```shell
pip install pytest
pip install pytest-cov
```

You can then run the software tests with the following command:

```shell
pytest ./iqmotion/tests/ --cov-config=.coveragerc --cov=iqmotion --cov-fail-under=90
```

The test will fail if coverage is under 90%

You can run the hardware tests with the following commands:

```shell
python run_hardware_tests.py speed --usb_handle=/dev/ttyUSB0
python run_hardware_tests.py servo --usb_handle=/dev/ttyUSB0
python run_hardware_tests.py step_dir --usb_handle=/dev/ttyUSB0
```

We use pylint and black to format this repository.

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

## Authors

- **Raphael Van Hoffelen**

See also the list of [contributors](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/contributors.md) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/LICENSE) file for details

## Acknowledgments

- Matt Piccoli for helping out debugging the architecture and continuously testing the API.
