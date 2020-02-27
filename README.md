# IQ Motion Python API

![Coverage](https://github.com/iq-motion-control/iq-module-communication-python/workflows//coverage.svg) ![Version](release_badge.svg)

This library is to talk to any IQ Control devices from mulititude of communication protocoles.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

All the prerequisited can be installed from ["requirement.txt"](requirement.txt).

```python
pip install requirements.txt
```

### Installing

You can install this library using "pip":

```python
pip install iqmotion
```

If you want to edit this library and/or run some tests, You can clone this repository locally on your computer.

## Running the tests

You will need the following packages to run the tests:

- pytest
- pytest-cov

You can install these packages with pip:

```python
pip install pytest
pip install pytest-cov
```

You can then run the tests with the following command:

```python
pytest --cov-config=.coveragerc --cov=iqmotion iqmotion --cov-fail-under=100
```

The test will fail if coverage is under 100%

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

- **Raphael Van Hoffelen**

See also the list of [contributors](contributors.md) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- Matt Piccoli for helping out debugging the architecture.
