from validator import Validator


class EmailValidator(Validator):
    email = "required|email"


class CellphoneValidator(Validator):
    phone = "cellphone"


class TextFieldOnlyValidator(Validator):
    name = "alphabet"


class DecimalValidator(Validator):
    decimal_value = "required|decimal"


class DigitsOnlyValidator(Validator):
    value = "required|digits"


class DocumentNumberValidator(Validator):
    id_number = "required|regex:^WR\\d{8}-\\d{2}-\\d{7}-\\d$"
