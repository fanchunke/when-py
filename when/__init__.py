from typing import Optional

from .rules import Options
from .when import Parser, Result


def new(options: Optional[Options] = None) -> Parser:
    if options is None:
        return Parser()
    return Parser(options=options)


__all__ = [
    "new",
    "Parser",
    "Result",
]
