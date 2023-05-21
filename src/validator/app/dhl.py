from .interface import IValidatable, ValidatedShipment


class DhlValidator(IValidatable):
    @property
    def STEPS(self):
        return (
            self.__validate_weight,
            self.__validate_dimensional_weight,
            self.__validate_length,
            self.__validate_other_sizes,
        )

    def validate(self) -> ValidatedShipment | None:
        for step in self.STEPS:
            if not step():
                return

        return ValidatedShipment(
            weight=self.weight,
            length=self.length,
            width=self.width,
            height=self.height,
            is_sortable=True,
        )

    def __validate_weight(self) -> bool:
        max_weight = 31.5
        return self.weight < max_weight

    def __validate_length(self) -> bool:
        max_length = 120
        return self.length < max_length

    def __validate_other_sizes(self) -> bool:
        max_other_sum = 200
        return self.width + self.height < max_other_sum

    def __validate_dimensional_weight(self) -> bool:
        max_dim_weight = 31.5
        dimensional_weight = self.length * self.width * self.height / 6000
        return dimensional_weight < max_dim_weight
