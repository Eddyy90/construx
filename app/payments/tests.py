import unittest

from django.core.urlresolvers import reverse
from django.test import Client

from .models import Payment


class PaymentViewTest(unittest.TestCase):
    "Some basic tests for our views"
    def setUp(self):
        self.client = Client()

    def testIndex(self):
        url = reverse('payments_payment_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
