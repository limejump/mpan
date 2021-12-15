from faker.providers import BaseProvider

from .helpers import generate


class MPANProvider(BaseProvider):
    def mpan(self) -> str:
        return generate()
