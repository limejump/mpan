# Development

If you only want to *use* this library, you can just ignore this section.  If
however you'd like to extend it or submit a pull request to fix a bug, keep
reading.


## Setting up a Local Development Environment

We're using [Poetry](https://python-poetry.org/), so if you want to make some
changes, you should install that and then just run `poetry install`.  This will
pull in all the development dependencies like `pytest`, `isort`, etc.


# Testing

When inside your virtualenv, just run:

```shell
$ pytest
```


## Deployment/Releases

To build, use Poetry:

```shell
$ poetry build
```

To publish a new release, use Poetry for that too:

```shell
$ poetry publish
```

...obviously you'll need permissions on PyPI to do that though 😉
