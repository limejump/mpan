# Generation

You may not be interested in parsing an MPAN, but rather would just like a way
to reliably generate a valid one a few thousand times.  For that, this library
has a provider fo both the [Faker](https://pypi.org/project/Faker/) and
[Mimesis](https://mimesis.name/) libraries:


## Faker

Faker support is available via the optional extra `faker`, so you must install
`mpan` like this to use it:

```shell
$ pip install mpan[faker]
```


### Example

```python
from faker import Faker

from mpan.generation.faker import MPANProvider


fake = Faker()
fake.add_provider(MPANProvider)

print(fake.mpan())
```


## Mimesis

Mimesis support is available via the optional extra `mimesis`, so you must
install `mpan` like this to use it:

```shell
$ pip install mpan[mimesis]
```


### Example

```python
from mimesis import Generic
from mimesis.locales import Locale

from mpan.generation.mimesis import MPANProvider


generic = Generic(locale=Locale.DEFAULT)
generic.add_provider(MPANProvider)

print(generic.mpan.generate())
```
