# These can't be handled at all by the library
UNPARSEABLE = (
    "Not an MPAN",
    "42",
)

# These look legit, but don't pass the validation
INVALID = (
    "2499999999990",  # Bad checksum
    "8699999999991",  # Bad distributor
    "991112221312345678907",  # Bad profile class
    "000002221312345678907",  # Bad mtc
)


# These are randomly generated.  Any correlation to a real MPAN is entirely
# coincidental.
VALID = (
    "069238I51470116845051",
    "01575R681049827101269",
    "04989PT43433899920164",
    "00709GFE2143967712809",
    "02116MEB2830997098859",
    "03968O6C1816273348119",
    "04603EXJ2146743072093",
    "0454742I1892941794350",
    "01947QUY1525379938096",
    "04962VE42544886475542",
)
