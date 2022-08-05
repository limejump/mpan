# Parsing & Validation

```python
from mpan.mpan import MPAN


mpan = MPAN("A valid MPAN")
```

Just import the library and pass it the MPAN you want to parse.  In response
you get a handy `MPAN` object with a number of convenient properties:


## The Basics

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


## The Top Line

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


## The Distributor

The `core` can also be broken up to look into the `distributor`, which is a
little tricky, since the distributor id can either refer to a DNO or an IDNO
both of which are similar, but slightly different in how we refer to them.
This library does its best to represent a unified interface to both:

```python
mpan = MPAN("2099999999993")

mpan.distributor                   # A Distributor instance
mpan.distributor.identifier        # "20"
mpan.distributor.gsp_group_ids     # ["_H"]
mpan.distributor.name              # "Scottish & Southern Electricity Networks"
mpan.distributor.participant_id    # "SOUT"
mpan.distributor.is_dno            # True
mpan.distributor.is_idno           # False
mpan.distributor.type              # "DNO"
mpan.distributor.is_valid          # True

mpan = MPAN("2499999999991")

mpan.distributor                   # A Distributor instance
mpan.distributor.identifier        # "24"
mpan.distributor.gsp_group_ids     # ["_A", "_B", "_C", "_D", "_E", "_F", "_G", "_H", "_J", "_K", "_L", "_M", "_N", "_P"]
mpan.distributor.name              # "Envoy"
mpan.distributor.participant_id    # "IPNL"
mpan.distributor.is_dno            # False
mpan.distributor.is_idno           # True
mpan.distributor.type              # "IDNO"
mpan.distributor.is_valid          # True
```


## Aliases

For people who want to limit the number of characters they're typing, we
recognise a few standard acronyms:

```python
mpan.pc    # Profile Class
mpan.mtc   # Meter Time Switch Code
mpan.llfc  # Line Loss Factor Class
```
