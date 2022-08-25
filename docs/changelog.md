# Changelog

## 2.0.0

* We rewrote the distribution portion of the parser to better reflect the n:1
  relationship between GSP groups and distributors.  The `.gsp_group_id`
  (`str`) is gone, replaced with `.gsp_groups` (`list[str]`).
* The API for DNOs and IDNOs are now the same, dropping properties like
  `.licensee` and `mpas_operator_id` in favour of a common `participant_id`.
  See the docs for specifics.


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
