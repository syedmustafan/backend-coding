from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """
        The index page loads properly
        """

        response = self.client.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matching_key_value/select.html')
