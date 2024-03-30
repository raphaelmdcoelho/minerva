import unittest
from unittest.mock import patch
from flask import Flask
import sys
import os

##TODO: need to simplify that:
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from api.v1.resources.articles import bp as articles_bp

class ArticlesBlueprintTestCase(unittest.TestCase):
    
    def setUp(self):
        """Create a new application for testing."""
        self.app = Flask(__name__)
        self.app.register_blueprint(articles_bp, url_prefix='/api/v1/resources')
        self.client = self.app.test_client()

    @patch('requests.post')
    def test_content_endpoint_success(self, mock_post):
        """Test the /content endpoint with a successful response."""

        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'choices': [{'text': 'Sample response from OpenAI.'}]}

        response = self.client.post('/api/v1/resources/content', json={'message': 'What is AI?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample response from OpenAI.', response.json['choices'][0]['text'])

    @patch('requests.post')
    def test_content_endpoint_no_message(self, mock_post):
        """Test the /content endpoint without 'message' provided."""
        response = self.client.post('/api/v1/resources/content', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'No message provided')

    @patch('requests.post')
    def test_content_endpoint_not_json(self, mock_post):
        """Test the /content endpoint with non-JSON content."""
        response = self.client.post('/api/v1/resources/content', data='This is not a JSON format', content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Request must be in JSON format')

if __name__ == '__main__':
    unittest.main()