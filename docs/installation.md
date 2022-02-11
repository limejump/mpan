# Installation

Getting up and running with `mpan` is easy.


## Requirements

This is a pure-python module with no external dependencies.  However, you'll
need to be running **Python 3.8** or higher.


## PyPI

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
