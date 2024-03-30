import unittest
from unittest.mock import patch
from flask import Flask
from flask_testing import TestCase
import os, sys

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from api.v1.resources.articles import bp as articles_bp

class MockResponse:
    def __init__(self):
        self.choices = [self.MockChoice()]

    class MockChoice:
        def __init__(self):
            self.message = self.MockMessage()

        class MockMessage:
            def __init__(self):
                self.content = 'Mock response from OpenAI'

class TestArticles(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.register_blueprint(articles_bp)
        return app

    @patch('api.v1.resources.articles.OpenAI')
    def test_content_endpoint(self, MockOpenAI):
        instance = MockOpenAI.return_value
        instance.chat.completions.create.return_value = MockResponse()

        response = self.client.post('/content', json={'message': 'Hello, world!'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Mock response from OpenAI')

if __name__ == '__main__':
    unittest.main()
