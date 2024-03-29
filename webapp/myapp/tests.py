from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.http import JsonResponse

# ensure that process_text view returns the expected JSON response when provided with sample input data
class RealTimeDataProcessingTestCase(TestCase):
    def test_process_text_view(self):
        """
        Test the process_text view for real-time data processing.
        """
        client = Client()
        response = client.post('/process-text/', {'text_input': 'Sample text'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('result' in response.json())
        self.assertTrue('sentiment' in response.json())
        self.assertTrue('entities' in response.json())
        
        self.assertIn('result', response.json())
        self.assertIn('sentiment', response.json())
        self.assertIn('sentiment_score', response.json())
        self.assertIn('personal_classification', response.json())
        self.assertIn('entities', response.json())
        self.assertIn('ranked_entities', response.json())
        self.assertIn('ensemble_result', response.json())
        self.assertIn('multiple_classification', response.json())
        self.assertIn('trustworthiness', response.json())
        self.assertIn('outdated_warning', response.json())

# if POST with malicious script, script tags are sanitized from the response.
class SecurityTestCase(TestCase):
    def test_csrf_protection(self):
        """
        Test CSRF protection for all POST requests.
        """
        client = Client(enforce_csrf_checks=True)
        response = client.post('/process-text/', {'text_input': 'Sample text'})
        self.assertEqual(response.status_code, 403)  # CSRF token required

    def test_xss_protection(self):
        """
        Test XSS protection for user inputs.
        """
        client = Client()
        malicious_input = '<script>alert("XSS Attack!");</script>'
        response = client.post('/process-text/', {'text_input': malicious_input})
        self.assertNotIn('<script>', response.content.decode())  # Ensure script tags are sanitized

# ensure that the home page renders successfully
class HomePageTestingTestCase(TestCase):
    def test_home_page(self):
        """
        Test the home page rendering.
        """
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')