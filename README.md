[![Limejump logo](https://raw.githubusercontent.com/limejump/mpan/master/logo.png)](https://limejump.com/)


# mpan

[![PyPI](https://img.shields.io/pypi/pyversions/mpan)](https://pypi.org/project/mpan)
[![PyPI](https://img.shields.io/pypi/wheel/mpan)](https://pypi.org/project/mpan)
[![License](https://img.shields.io/pypi/l/mpan)](https://mit-license.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![100% Coverage](https://img.shields.io/badge/coverage-100%25-4ec820.svg)

A library to help you parse the UK energy industry's MPAN number format.


## Parsing & Validation

```python
from mpan.mpan import MPAN


mpan = MPAN("A valid MPAN")
```

Just import the library and pass it the MPAN you want to parse.  In response
you get a handy `MPAN` object with a number of convenient properties:


### The Basics

The most common use is likely to be in examining the "core":

```python
mpan = MPAN("001112221312345678907")

mpan.top_line    # "00111222"
mpan.core        # "1312345678907"
mpan.identifier  # "12345678"
mpan.is_short    # False
mpan.is_long     # True
mpan.as_short    # "1312345678907"

mpan = MPAN("1312345678907")

mpan.top_line    # None
mpan.core        # "1312345678907"
mpan.identifier  # "12345678"
mpan.is_short    # True
mpan.is_long     # False
mpan.as_short    # "1312345678907"
```


### The Top Line

You can also go deeper though, and interrogate the top line:

```python
mpan = MPAN("001112221312345678907")

mpan.profile_class                       # A ProfileClass instance
mpan.profile_class.identifier            # "00"
mpan.profile_class.description           # "Half-hourly supply (import and export)"
mpan.profile_class.is_valid              # True

mpan.meter_time_switch_code              # A MeterTimeSwitchCode instance
mpan.meter_time_switch_code.identifier   # "111"
mpan.meter_time_switch_code.description  # "DNO specific"
mpan.meter_time_switch_code.is_valid     # True

mpan.line_loss_factor_class              # "222"
```

Note however that if you don't supply a long MPAN, this library can't help you:

```python
mpan = MPAN("1312345678907")

mpan.profile_class           # None
mpan.meter_time_switch_code  # None
mpan.line_loss_factor_class  # None
```


### The Distributor

The `core` can also be broken up to look into the `distributor`, which is a
little tricky, since the distributor id can either refer to a DNO (which has a
known set of properties) or an IDNO (which has a different set).  We handle
this discrepancy by returning `None` in cases where the requested information
is unavailable:

```python
mpan = MPAN("2099999999993")

mpan.distributor                   # A Distributor instance
mpan.distributor.identifier        # "20"
mpan.distributor.area              # "Southern England"
mpan.distributor.gsp_group_id      # "_H"
mpan.distributor.operator          # "Scottish & Southern Electricity Networks"
mpan.distributor.participant_id    # "SOUT"
mpan.distributor.is_dno            # True
mpan.distributor.is_idno           # False
mpan.distributor.is_valid          # True
mpan.distributor.licensee          # None
mpan.distributor.mpas_operator_id  # None
mpan.distributor.name              # None

mpan = MPAN("2499999999991")

mpan.distributor                   # A Distributor instance
mpan.distributor.identifier        # "24"
mpan.distributor.area              # None
mpan.distributor.gsp_group_id      # None
mpan.distributor.operator          # None
mpan.distributor.participant_id    # None
mpan.distributor.is_dno            # False
mpan.distributor.is_idno           # True
mpan.distributor.is_valid          # True
mpan.distributor.licensee          # "Independent Power Networks"
mpan.distributor.mpas_operator_id  # "IPNL"
mpan.distributor.name              # "Envoy"
```


### Aliases

For people who want to limit the number of characters they're typing, we
recognise a few standard acronyms:

```python
mpan.pc    # Profile Class
mpan.mtc   # Meter Time Switch Code
mpan.llfc  # Line Loss Factor Class
```


### Validation Options

You've got choices for validation.  `.is_valid()` will check your MPAN string
and return a boolean value indicating whether it's valid or not, while you can
call `.check()` on an `MPAN` instance, which will explode with an
`InvalidMpanError` if your string doesn't check out.

> An important note about validation
>
> There are four aspects of validation performed by the validation checks
> below: the profile class and meter time switch code (if provided as part of
> the top line in a long MPAN) will be checked against a list of known values,
> the distributor from the core will be similarly checked, and finally the
> formula for the check digit will be applied.

```python
from mpan.exceptions import InvalidMPANError
from mpan.mpan import MPAN


MPAN("2499999999991").is_valid          # True
MPAN("2499999999990").is_valid          # False  (bad checksum)
MPAN("8699999999991").is_valid          # False  (bad distributor)
MPAN("001112221312345678907").is_valid  # True
MPAN("991112221312345678907").is_valid  # False  (bad profile class)
MPAN("000002221312345678907").is_valid  # False  (bad meter time switch code)

MPAN("I am not an MPAN")                # InvalidMPANError

try:
    MPAN("2499999999991").check()  # Returns None
    MPAN("2499999999990").check()  # Raises an InvalidMPANError
except InvalidMPANError:
    print("This MPAN is broken")
```

There's also a shortcut if you just want validation:

```python
from mpan.helpers import is_valid


is_valid("2499999999991")     # True
is_valid("2499999999990")     # False
is_valid("I am not an MPAN")  # False
```

### Generation

You can also use this library to generate valid MPANs via [Faker](https://github.com/joke2k/faker)
or [Mimesis](https://mimesis.name/):


#### Faker

```python
from faker import Faker

from mpan.generation.faker import MPANProvider


fake = Faker()
fake.add_provider(MPANProvider)
fake.mpan()
```


#### Mimesis

```python
from mimesis import Generic
from mimesis.locales import Locale

from mpan.generation.mimesis import MPANProvider


generic = Generic(locale=Locale.DEFAULT)
generic.add_provider(MPANProvider)
generic.mpan.generate()
```


## Generation

You may not be interested in parsing an MPAN, but rather would just like a way
to reliably generate a valid one a few thousand times.  For that, this library
has a provider fo both the [Faker](https://pypi.org/project/Faker/) and
[Mimesis](https://mimesis.name/) libraries:


### Faker

Faker support is available via the optional extra `faker`, so you must install
`mpan` like this to use it:

```shell
$ pip install mpan[faker]
```


#### Example

```python
from faker import Faker

from mpan.generation.faker import MPANProvider


fake = Faker()
fake.add_provider(MPANProvider)

print(fake.mpan())
```


### Mimesis

Mimesis support is available via the optional extra `mimesis`, so you must
install `mpan` like this to use it:

```shell
$ pip install mpan[mimesis]
```


#### Example

```python
from mimesis import Generic
from mimesis.locales import Locale

from mpan.generation.mimesis import MPANProvider


generic = Generic(locale=Locale.DEFAULT)
generic.add_provider(MPANProvider)

print(generic.mpan.generate())
```


## Installation

It's on PyPI, so you can install it with `pip`:

```shell
$ pip install mpan
```

This will give you the base version of the library which can only do parsing
and validation.  If you also want support for generation, you need to specify
*which* generation method you want to use.  It will be rolled in as a dependency:

```shell
$ pip install mpan[faker]
```

or

```shell
$ pip install mpan[mimesis]
```


## Requirements

This is a pure-python module with no external dependencies.  However, you'll
need to be running Python 3.8 or higher.


## Development

### Setting up a Local Development Environment

We're using [Poetry](https://python-poetry.org/), so if you want to make some
changes, you should install that and then just run `poetry install`.  This will
pull in all the development dependencies like `pytest`, `isort`, etc.


## Testing

When inside your virtualenv, just run:

```shell
$ pytest
```


### Deployment/Releases

To build, use Poetry:

```shell
$ poetry build
```

To publish a new release, use Poetry for that too:

```shell
$ poetry publish
```


## External Documentation

This is based largely on the [Wikipedia article](https://en.wikipedia.org/wiki/Meter_Point_Administration_Number)
on the MPAN standard.  The validation code for example is cribbed right from
there.


## Changelog


### 1.1.0

* Added support for automatic generation of valid MPANs with either Faker or
  Mimesis.


### 1.0.4

* Minor update to the validation error message.


### 1.0.3

* Bugfix: Comparing two identical MPAN objects now returns boolean `True`,
  while comparing an MPAN object to a string of the same value returns `False`.
* Added lots more documentation to the README.


### 1.0.2

* `.is_valid()` was amended to validate the top row as well.
* `is_valid()` now returns a boolean rather than potentially throwing an
  `InvalidMPANError`.


### 1.0.1

* Minor change to use a new contact email


### 1.0.0

* Initial release
