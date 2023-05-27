import decimal

from .interface import CURRENCY, EstimatedShipment, IEstimatable, Money


class DhlEstimator(IEstimatable):
    @property
    def STEPS(self):
        return (
            self.__get_base_price,
            self.__add_not_sortable_charge,
        )

    @property
    def CURRENCY(self):
        return CURRENCY.EUR

    def estimate(self) -> EstimatedShipment | None:
        amount = decimal.Decimal(0)
        for step in self.STEPS:
            result = step()
            if result is None:
                raise ValueError("Price cannot be calculated")
            amount += result

        return EstimatedShipment(
            weight=self.weight,
            length=self.length,
            width=self.width,
            height=self.height,
            is_sortable=True,
            price=Money(amount=amount, currency=self.CURRENCY),
        )

    def __get_base_price(self) -> decimal.Decimal:
        if self.weight <= 10.0:
            return decimal.Decimal(10.0)
        elif self.weight <= 20.0:
            return decimal.Decimal(20.0)
        elif self.weight <= 31.5:
            return decimal.Decimal(50.0)

        raise ValueError("Weight is too big")

    def __add_not_sortable_charge(self) -> decimal.Decimal:
        if self.is_sortable:
            return decimal.Decimal(0.0)

        return decimal.Decimal(12.30)
