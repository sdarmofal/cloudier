from enum import Enum
from typing import TypedDict

from .dhl import DhlValidator


class CARRIERS(str, Enum):
    DHL = "DHL"


class ValidShipment(TypedDict):
    carrier: CARRIERS
    weight: float
    length: float
    width: float
    height: float
    is_sortable: bool


class Validator:
    VALIDATORS = {CARRIERS.DHL: DhlValidator}

    def __init__(self, weight: float, length: float, width: float, height: float):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

    def validate(self) -> list[ValidShipment]:
        valid_shipments: list[ValidShipment] = []
        for carrier, validator in self.VALIDATORS.items():
            if validator(self.weight, self.length, self.width, self.height).validate():
                valid_shipments.append(
                    ValidShipment(
                        carrier=carrier,
                        weight=self.weight,
                        length=self.length,
                        width=self.width,
                        height=self.height,
                        is_sortable=True,
                    )
                )

        return valid_shipments
