import string
from decimal import Decimal


def currency_to_denom(currency: string) -> string:
    lowercase_currency = currency.lower()

    currency_map = {
        "ust": "uusd"
    }

    return currency_map[lowercase_currency]


def get_u_amount(amount: Decimal) -> float:
    return float(amount) * 1000000
