import abc
from typing import Callable, TypedDict


class ValidatedShipment(TypedDict):
    weight: float
    length: float
    width: float
    height: float
    is_sortable: bool


class IValidatable(abc.ABC):
    def __init__(self, weight: float, length: float, width: float, height: float):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

    @property
    @abc.abstractmethod
    def STEPS(self) -> tuple[Callable, ...]:
        raise NotImplementedError

    @abc.abstractmethod
    def validate(self) -> ValidatedShipment | None:
        raise NotImplementedError
