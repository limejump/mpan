from mimesis.providers.base import BaseProvider

from .helpers import generate


class MPANProvider(BaseProvider):
    class Meta:
        name = "mpan"

    @staticmethod
    def generate() -> str:
        return generate()
