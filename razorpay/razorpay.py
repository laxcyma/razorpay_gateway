from django.conf import settings
from django.http import HttpResponseRedirect

from .conf import conf

from fleio.billing.gateways.decorators import gateway_action, staff_gateway_action
from fleio.billing.gateways import exceptions as gateway_exceptions

from fleio.core.utils import fleio_join_url


def process_test_payment(test_mode):
    pass


@gateway_action(methods=['GET'])
def pay_invoice(request):
    invoice_id = request.query_params.get('invoice')

    try:
        process_test_payment(test_mode=conf.test_mode)
    except Exception as create_payment_exception:
        # handle possible exception
        raise gateway_exceptions.InvoicePaymentException(
            message=str(create_payment_exception),
            invoice_id=invoice_id
        )
    # redirect to invoice
    relative_url = 'billing/invoices/{}'.format(invoice_id)
    return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, relative_url))




