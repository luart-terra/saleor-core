from saleor.payment.gateways.utils import require_active_plugin
from saleor.payment.interface import GatewayConfig, GatewayResponse, PaymentData, \
    TokenConfig
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

from . import get_client_token, process_payment, authorize, capture, void, \
    refund, confirm

GATEWAY_NAME = "Paywith Terra"


class PaywithTerraGatewayPlugin(BasePlugin):
    PLUGIN_NAME = GATEWAY_NAME
    PLUGIN_ID = "luart.payments.paywith_terra"

    DEFAULT_CONFIGURATION = [
        {"name": "API Key (token)", "value": None},
        {"name": "Terra address", "value": None},
        {"name": "Webhook URL", "value": None},
        {"name": "Redirect URL", "value": None},
    ]

    CONFIG_STRUCTURE = {
        "API Key (token)": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": "API key from your PaywithTerra account page.",
            "label": "API Key (token)",
        },
        "Terra address": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "Your shop wallet address on the Terra blockchain to "
                         "receiving payments.",
            "label": "Terra address",
        },
        "Webhook URL": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "URL that should be used when coming back from payment page.",
            "label": "Webhook URL",
        },
        "Redirect URL": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "URL that should be used by payment provider "
                         "to inform that payment was successful.",
            "label": "Redirect URL",
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        configuration = {item["name"]: item["value"] for item in self.configuration}

        self.config = GatewayConfig(
            gateway_name=GATEWAY_NAME,
            supported_currencies="UST",
            store_customer=True,
            auto_capture=True,
            connection_params=configuration
        )

    def _get_gateway_config(self):
        return self.config

    @require_active_plugin
    def authorize_payment(
            self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return authorize(payment_information, self._get_gateway_config())

    @require_active_plugin
    def capture_payment(
            self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return capture(payment_information, self._get_gateway_config())

    @require_active_plugin
    def confirm_payment(
            self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return confirm(payment_information, self._get_gateway_config())

    @require_active_plugin
    def refund_payment(
            self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return refund(payment_information, self._get_gateway_config())

    @require_active_plugin
    def void_payment(
            self, payment_information: "PaymentData", previous_value
    ) -> "GatewayResponse":
        return void(payment_information, self._get_gateway_config())

    @require_active_plugin
    def process_payment(
            self, payment_information: PaymentData, previous_value
    ) -> GatewayResponse:
        return process_payment(payment_information, self._get_gateway_config())

    @require_active_plugin
    def get_supported_currencies(self, previous_value):
        return [c.strip() for c in self.config.supported_currencies.split(",")]

    @require_active_plugin
    def get_payment_config(self, previous_value):
        return []

    @require_active_plugin
    def get_client_token(self, token_config: TokenConfig, previous_value):
        return get_client_token()

    @require_active_plugin
    def token_is_required_as_payment_input(self, previous_value):
        return False
