__all__ = []


class ConverterNumbersCatalog:
    regex = r"[1-9][0-9]*"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return value
