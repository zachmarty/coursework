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
        if tmp_val <= 0:
            raise ValidationError("price cannot be less than 0")


class TextLengthValidator:
    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        try:
            tmp_val = value[self.field]
        except:
            ValidationError("text field error")
        if type(tmp_val) is None:
            raise ValidationError("text cannot be blank")
        if len(tmp_val) > 1000:
            raise ValidationError("text is too big")
