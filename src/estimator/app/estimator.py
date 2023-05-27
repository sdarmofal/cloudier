from enum import Enum

from .app_logger import app_logger
from .dhl import DhlEstimator
from .interface import EstimatedShipment


class EstimationError(Exception):
    pass


class CARRIER(str, Enum):
    DHL = "DHL"


class Estimator:
    ESTIMATORS = {CARRIER.DHL: DhlEstimator}

    def __init__(
        self, weight: float, length: float, width: float, height: float, is_sortable
    ):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.is_sortable = is_sortable

    def estimate(self) -> tuple[CARRIER, EstimatedShipment]:
        estimated_shipments: list[tuple[CARRIER, EstimatedShipment]] = []
        for carrier, estimator in self.ESTIMATORS.items():
            try:
                estimated_shipment = estimator(
                    self.weight, self.length, self.width, self.height, self.is_sortable
                ).estimate()
                estimated_shipments.append((carrier, estimated_shipment))
            except ValueError as exception:
                app_logger.warning(
                    f"Cannot estimate shipment for {carrier}", exc_info=exception
                )

        if not estimated_shipments:
            raise EstimationError("Cannot find any shipment estimations")

        return self.__find_best_price(estimated_shipments)

    def __find_best_price(
        self, estimated_shipments: list[tuple[CARRIER, EstimatedShipment]]
    ):
        estimated_shipments.sort(key=lambda x: x[1]["price"].amount)
        best_price = estimated_shipments[0]
        return best_price[0].value, best_price[1]
