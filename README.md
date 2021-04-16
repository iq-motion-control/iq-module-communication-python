# IQ Motion Python API

![Python Build](https://github.com/iq-motion-control/iq-module-communication-python/workflows/Python%20Build/badge.svg)
[![codecov](https://codecov.io/gh/iq-motion-control/iq-module-communication-python/branch/master/graph/badge.svg)](https://codecov.io/gh/iq-motion-control/iq-module-communication-python)
![tag](https://img.shields.io/github/v/tag/iq-motion-control/iq-module-communication-python)
![release](https://img.shields.io/github/release/iq-motion-control/iq-module-communication-python/all.svg)

This library is to talk to any IQ Control devices from mulititude of communication protocols.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.  
To Learn more about this API, Read the [Communications API Documentation](https://iq-motion-control-iqmotion.readthedocs-hosted.com/en/latest/) 

### Prerequisites

#### Pipenv

Read the second part of [this](https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c) and [this](https://pipenv-fork.readthedocs.io/en/latest/basics.html) for more information on pipenv.

Windows and mac users:

- [installing pipenv](https://medium.com/@mahmudahsan/how-to-use-python-pipenv-in-mac-and-windows-1c6dc87b403e)

Linux users:

- [installing pipenv](https://github.com/pypa/pipenv)

### Installing

You can install this library using "pipenv" or "pip":

```bash
pipenv install iqmotion
```

or

```bash
pip install iqmotion
```

If you want to edit this library and/or run some tests, You can clone this repository locally on your computer.

### Submodule

If you are using this repository as a submodule, make sure to make a symbolic link:

```bash
ln -s python_api/iqmotion iqmotion
```

If you prefer **not** to use symbolic links, you could dynamically append the library to your system PATH at runtime by following along with the example below:

```bash
├── examples 
│   ├── api_testing.py <---------------(current python script)
│   ├── async_example.py
│   ├── multi_turn_example.py
│   └── propeller_example.py
├── iqmotion   <-----------------------(IQMOTION API LIBRARY)
│   ├── client_entries
│   │   ├── client_entry_data.py
│   │   ├── client_entry.py
│   │   ├── dictionary_client_entry.py
│   │   ├── __init__.py
│   │   └── process_client_entry.py
│   ├── clients
```

If you wanted to run api_testing.py from the examples Directory, you would need to append the iqmotion library to the system path at the top of my api_testing.py script:

```python
import sys

#  Adds the parent directory to the system path 
# (Same location that the iqmotion library is located)
sys.path.append("../") 
```

## Running the tests

You will need the following packages to run the tests:

- pytest
- pytest-cov

They should be already installed with pipenv.

You can then run the software tests with the following command:

```shell
pytest ./iqmotion/tests/ --cov-config=.coveragerc --cov=iqmotion --cov-fail-under=100
```

The test will fail if coverage is under 100%

You can run the hardware tests with the following commands:

```shell
python run_hardware_tests.py speed --usb_handle=/dev/ttyUSB0
python run_hardware_tests.py servo --usb_handle=/dev/ttyUSB0
python run_hardware_tests.py step_dir --usb_handle=/dev/ttyUSB0
```

## Clean Code

### Formatting

We use [black](https://github.com/psf/black) as a formatter. It does everything for you and it should be installed with the dev packages of pipenv.  
I recommend setting up your IDE to format with black when saving. Vscode has a known issue sometimes with new .py files where you need to run black in the terminal first
You can also run black from the terminal with:

```bash
black ./
```

### Linting

We use [pylint](https://www.pylint.org/) as a linter. It does everything for you and it should be installed with the dev packages of pipenv.  
We have a [.pylintrc](./.pylintrc) file that setups your pylint for you.

I would recommend to set up your IDE to use pylint automatically (vscode should find the .pylintrc automatically).

Sometimes pylint shouts at out some errors you do not wantc you can disbale a pylint error locally in a file/method/class with a comment like this:

```python
# pytlint: disable=my-error
```

You can also run pylint from the terminal with the following command:

```bash
pylint your_project_directory
```

## New Releases

It is really easy to create a new release, simply run the following script and follow the prompt:

(You might need to run the following command to use a bash script in windows):

```bash
dos2unix ./ci_scripts/new_release.sh
```

```bash
./ci_scripts/new_release.sh
```

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Raphael Van Hoffelen**
- **Malik B. Parker**

See also the list of [contributors](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/contributors.md) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/iq-motion-control/iq-module-communication-python/blob/master/LICENSE) file for details

## Acknowledgments

- Matt Piccoli for helping out debugging the architecture and continuously testing the API.
