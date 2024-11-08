import unittest

from django.core.urlresolvers import reverse
from django.test import Client

from .models import Work


class WorkViewTest(unittest.TestCase):
    "Some basic tests for our views"
    def setUp(self):
        self.client = Client()

    def testIndex(self):
        url = reverse('works_work_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
