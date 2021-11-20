import requests

from .utils import currency_to_denom, get_u_amount
from saleor.payment.interface import GatewayConfig

PAYWITH_TERRA_API_URL = "https://paywithterra.com/api"


def create_order(config: GatewayConfig, amount, currency, payment_id):
    request = requests.post(PAYWITH_TERRA_API_URL + "/order/create",
                            json={
                                "address": config.connection_params["Terra address"],
                                "return_url": config.connection_params["Redirect URL"]
                                + "/checkout/payment-confirm?paymentId=" + str(payment_id),
                                "webhook": config.connection_params["Webhook URL"],
                                "webhook_json": True,
                                "memo": "Payment:" + str(payment_id),
                                "amount": get_u_amount(amount),
                                "denom": currency_to_denom(currency),
                            },
                            headers={
                                "Authorization": "Bearer " + config.connection_params[
                                    "API Key (token)"]})

    return request.json()


def is_order_paid(order_id, api_key) -> bool:
    request = requests.get(PAYWITH_TERRA_API_URL + "/order/" + order_id + "/status",
                           headers={"Authorization": "Bearer " + api_key})
    response = request.json()

    if response['is_paid']:
        return True

    return False
