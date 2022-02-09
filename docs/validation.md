# Validation Options

You've got choices for validation.  `.is_valid()` will check your MPAN string
and return a boolean value indicating whether it's valid or not, or you can
call `.check()` on an `MPAN` instance, which will explode with an
`InvalidMpanError` if your string doesn't check out.

!!! note

    **An important note about validation**

    There are four aspects of validation performed by the validation checks
    below: the profile class and meter time switch code (if provided as part of
    the top line in a long MPAN) will be checked against a list of known values,
    the distributor from the core will be similarly checked, and finally the
    formula for the check digit will be applied.

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


## Helpers

There's also a shortcut if you just want validation:

```python
from mpan.helpers import is_valid


is_valid("2499999999991")     # True
is_valid("2499999999990")     # False
is_valid("I am not an MPAN")  # False
```
