# Helium Api Wrapper

[![PyPI](https://img.shields.io/pypi/v/helium-api-wrapper.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/helium-api-wrapper.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/helium-api-wrapper)][python version]
[![License](https://img.shields.io/pypi/l/helium-api-wrapper)][license]

[![Read the documentation at https://helium-api-wrapper.readthedocs.io/](https://img.shields.io/readthedocs/helium-api-wrapper/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Test](https://github.com/emergotechnologies/helium-api-wrapper/workflows/Test/badge.svg)][test]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/helium-api-wrapper/
[status]: https://pypi.org/project/helium-api-wrapper/
[python version]: https://pypi.org/project/helium-api-wrapper
[read the docs]: https://helium-api-wrapper.readthedocs.io/
[test]: https://github.com/emergotechnologies/helium-api-wrapper/actions?workflow=Test
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- Load data from the Helium Blockchain API
  - Get hotspots by address
  - Get hotspots by location
  - Get a list of hotspots
  - Get challenges of a hotspot
  - Get a list of challenges
- Load Data from the Helium Console API
  - Get device information by uuid

## Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/)

## Installation

You can install _Helium Api Wrapper_ via [pip] from [PyPI]:

```console
$ pip install helium-api-wrapper
```

## Usage

You can import different modules to load data from the Helium Blockchain API or the Helium Console API.

```python
from helium_api_wrapper import hotspots, devices

hotspots.get_hotspot_by_address("some_address")
devices.get_device_by_uuid("some_uuid")
```

In order to use the Device API, you need to set the `API_KEY` environment variable. 
It is also possible to set different API endpoints for the Helium Blockchain API and the Helium Console API.

```python

```console

You can run the wrapper as a python module:

```
python -m helium_api_wrapper --help
python -m helium_api_wrapper get-hotspots
python -m helium_api_wrapper get-hotspot --address your-hotspot-address
```

To personalise the settings command the file (using -, -- or CAPS to specify your settings) in a preferred terminal.
To list all possible settings run the --help command.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Helium Api Wrapper_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/emergotechnologies/helium-api-wrapper/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/emergotechnologies/helium-api-wrapper/blob/main/LICENSE
[contributor guide]: https://github.com/emergotechnologies/helium-api-wrapper/blob/main/CONTRIBUTING.md
[command-line reference]: https://helium-api-wrapper.readthedocs.io/en/latest/usage.html
