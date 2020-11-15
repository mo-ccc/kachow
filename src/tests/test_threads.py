import unittest
from main import create_app, db
import commands

class test_endpoints(unittest.TestCase):
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.drop_all()
        db.create_all()
        
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])
        
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        db.create_all()
        cls.app_context.pop()
        
    def test_root(self):
        response = self.client.get('/threads/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)