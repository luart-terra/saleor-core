import uuid

from saleor.payment import TransactionKind
from saleor.payment.interface import GatewayResponse, GatewayConfig, PaymentData, \
    PaymentMethodInfo

from .client import create_order


def get_client_token(**_):
    return str(uuid.uuid4())


def refund(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    print('refund')

    error = None
    success = True

    if not success:
        error = "Unable to process refund"

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.REFUND,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
    )


def authorize(payment_information: PaymentData,
              config: GatewayConfig) -> GatewayResponse:
    print('authorize')

    success = True
    error = None
    extra_data = {}
    transaction_id = ""

    order = create_order(config=config,
                         amount=payment_information.amount,
                         currency=payment_information.currency,
                         payment_id=payment_information.payment_id
                         )
    print(payment_information)
    print(config)
    print(order)

    if "uuid" not in order:
        error = "Unable to register order"
        success = False
    else:
        transaction_id = order['uuid']
        extra_data = {
            "terra_transaction_id": order['uuid']
        }

    return GatewayResponse(
        is_success=success,
        action_required=bool(extra_data),
        action_required_data=extra_data,
        kind=TransactionKind.AUTH,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=transaction_id,
        raw_response=order,
        error=error,
        payment_method_info=PaymentMethodInfo(
            name="Paywith Terra",
            type="paywith_terra",
        ),
    )


def void(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    print('void')

    error = None
    success = True

    if not success:
        error = "Unable to void the transaction."

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.VOID,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
    )


def confirm(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    print('confirm')

    error = None
    success = True

    if not success:
        error = "Unable to process capture"

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.CAPTURE,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
    )


def capture(payment_information: PaymentData, config: GatewayConfig) -> GatewayResponse:
    print('capture')

    error = None
    success = True

    if not success:
        error = "Unable to process capture"

    return GatewayResponse(
        is_success=success,
        action_required=False,
        kind=TransactionKind.CAPTURE,
        amount=payment_information.amount,
        currency=payment_information.currency,
        transaction_id=payment_information.token or "",
        error=error,
        payment_method_info=PaymentMethodInfo(
            name="Paywith Terra",
            type="paywith_terra",
        ),
    )


def process_payment(payment_information: PaymentData,
                    config: GatewayConfig) -> GatewayResponse:
    print('process_payment')

    return authorize(payment_information, config)
