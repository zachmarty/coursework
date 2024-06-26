

from typing import Any

from rest_framework.exceptions import ValidationError


class PriceValidator:
    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        try:
            tmp_val = value[self.field]
        except:
            ValidationError("price field error")
        if type(tmp_val) is None:
            raise ValidationError("price cannot be blank")
        if tmp_val > 2147483647:
            raise ValidationError("price is too big")
    