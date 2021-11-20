import logging
from decimal import Decimal

from saleor.payment.gateways.utils import require_active_plugin
from saleor.payment.interface import GatewayConfig, GatewayResponse
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

GATEWAY_NAME = "Paywith Terra"

logger = logging.getLogger(__name__);


class PaywithTerraGatewayPlugin(BasePlugin):
    PLUGIN_NAME = GATEWAY_NAME
    PLUGIN_ID = "pf1gura.payments.paywith_terra"

    DEFAULT_CONFIGURATION = [
        {"name": "API Key (token)", "value": None},
        {"name": "Terra address", "value": None},
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

    # See if needed
    def get_supported_currencies(self, previous_value):
        return [c.strip() for c in self.config.supported_currencies.split(",")]

    @require_active_plugin
    def get_payment_config(self, previous_value):
        return []

    @require_active_plugin
    def process_payment(self) -> GatewayResponse:
        return GatewayResponse(
            is_success=True,
            transaction_id="TestID",
            currency=self.config.supported_currencies,
            amount=Decimal("0.01"),
            kind="INITIATED",
            error=None,
            action_required=False,
        )
