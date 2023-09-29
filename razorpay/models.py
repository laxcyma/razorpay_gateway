import razorpay

from django.db import models

from common.encryption.utils import FleioEncryption
from common.logger import get_fleio_logger
from fleio.billing.gateways.razorpay.conf import conf
from fleio.billing.gateways.utils import format_card_exp
from fleio.billing.models import Invoice
from fleio.core.models import Client
from fleio.core.utils import RandomId

LOG = get_fleio_logger(__name__)


class FleioPaymentIntent(models.Model):
    id = models.BigIntegerField(unique=True, default=RandomId('razorpay.FleioPaymentIntent'), primary_key=True)
    invoice = models.OneToOneField(
        Invoice, on_delete=models.CASCADE, db_index=True, related_name='+'
    )
    api_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    razorpay_id = models.CharField(max_length=1024, null=False, blank=False)
    client_secret = models.CharField(max_length=1024, null=False, blank=False)
    has_setup_future_usage = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.client_secret = FleioEncryption.encrypt(self.client_secret)
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def get_client_secret(self) -> dict:
        return FleioEncryption.decrypt(value=self.client_secret)
