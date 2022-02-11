# Changelog


## 1.1.0

* Added support for automatic generation of valid MPANs with either Faker or
  Mimesis.


## 1.0.4

* Minor update to the validation error message.


## 1.0.3

* Bugfix: Comparing two identical MPAN objects now returns boolean `True`,
  while comparing an MPAN object to a string of the same value returns `False`.
* Added lots more documentation to the README.


## 1.0.2

* `.is_valid()` was amended to validate the top row as well.
* `is_valid()` now returns a boolean rather than potentially throwing an
  `InvalidMPANError`.


## 1.0.1

* Minor change to use a new contact email


## 1.0.0

* Initial release
