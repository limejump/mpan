[![Limejump logo](https://raw.githubusercontent.com/limejump/mpan/master/logo.png)](https://limejump.com/)


# mpan

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`mpan` is a library to help you parse the UK energy industry's MPAN number format.


## How it works

```python
from mpan import InvalidMPANError, MPAN


mpan = MPAN("018011002012345678385")

print(mpan.core)  # 2012345678385
print(mpan.identifier)  # 12345678
print(mpan.is_short)  # False
print(mpan.profile_class.description)  # "Domestic unrestricted"
print(mpan.distributor.is_dno)  # True
print(mpan.distributor.area)  # "Southern England"

if mpan.is_valid:
    print("Looks good to me!")

try:
    mpan.check()
except InvalidMPANError:
    print("This MPAN is broken")
```

There's also a shortcut if you just want validation:

```python
from mpan import is_valid


if is_valid("<an MPAN string>"):
    print("Looks good to me too!")
```


## Installation

It's on PyPI:

```shell
$ pip install mpan
```


## Requirements

This is a pure-python module with no external dependencies.  However, you'll
need to be running Python 3.8 or higher.


## Development

### Setting up a Local Development Environment

We're using [Poetry](https://python-poetry.org/), so if you want to make some
changes, you should install that and then just run `poetry install`.  This will
pull in all the development dependencies like `pytest`, `isort`, etc.


### Deployment/Releases

To build, use Poetry:

```shell
$ poetry build
```

To publish a new release, use Poetry for that too:

```shell
$ poetry publish
```


## Testing

When inside your virtualenv, just run:

```shell
$ pytest
```


## External Documentation

This is based largely on the [Wikipedia article](https://en.wikipedia.org/wiki/Meter_Point_Administration_Number)
on the MPAN standard.  The validation code for example is cribbed right from
there.
