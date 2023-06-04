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

    def __init__(self, valid_shipments: list[dict]):
        self.valid_shipments = valid_shipments

    def estimate(self) -> tuple[CARRIER, EstimatedShipment]:
        estimated_shipments: list[tuple[CARRIER, EstimatedShipment]] = []
        for valid_shipment in self.valid_shipments:
            carrier: CARRIER = CARRIER[valid_shipment["carrier"]]
            try:
                estimator = self.ESTIMATORS[carrier]
                estimated_shipment = estimator(
                    valid_shipment["weight"],
                    valid_shipment["length"],
                    valid_shipment["width"],
                    valid_shipment["height"],
                    valid_shipment["is_sortable"],
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
