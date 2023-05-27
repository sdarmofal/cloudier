import abc
import dataclasses
import decimal
from enum import Enum
from typing import Callable, TypedDict


class CURRENCY(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    RUB = "RUB"
    PLN = "PLN"


@dataclasses.dataclass(frozen=True)
class Money:
    amount: decimal.Decimal
    currency: CURRENCY


class EstimatedShipment(TypedDict):
    weight: float
    length: float
    width: float
    height: float
    is_sortable: bool
    price: Money


class IEstimatable(abc.ABC):
    def __init__(
        self,
        weight: float,
        length: float,
        width: float,
        height: float,
        is_sortable: bool,
    ):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.is_sortable = is_sortable

    @property
    @abc.abstractmethod
    def STEPS(self) -> tuple[Callable, ...]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def CURRENCY(self) -> CURRENCY:
        raise NotImplementedError

    @abc.abstractmethod
    def estimate(self) -> EstimatedShipment | None:
        raise NotImplementedError
