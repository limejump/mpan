class Subsection:
    """
    A string-like object that includes additional information we know based on
    the identifier.
    """

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def __str__(self) -> str:
        return self.identifier

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.identifier}"

    def __bool__(self) -> bool:
        return self.is_valid

    @property
    def is_valid(self) -> bool:
        raise NotImplementedError()
