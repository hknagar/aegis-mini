from typing import TypedDict


class AegisState(TypedDict, total=False):

    question: str
    route: str
    result: object