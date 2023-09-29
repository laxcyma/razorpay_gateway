from django.conf import settings


class Conf(object):
    def __init__(self):
        self.razorpay_settings = getattr(settings, 'RAZORPAY_SETTINGS', {})
        self.test_mode = self.razorpay_settings.get('test_mode')
        self.secret_key = self.razorpay_settings.get('secret_key')
        self.callback_url = self.razorpay_settings.get('callback_url')


conf = Conf()
