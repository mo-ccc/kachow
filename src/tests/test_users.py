from main import create_app, db
import unittest
import commands
from tests.super_test import BaseTest

class TestUsers(BaseTest, unittest.TestCase):
    '''
    Pass the class 'test_endpoints' as the subclass
    into the super method
    '''
    @classmethod
    def setUpClass(cls):
        super(__class__, cls).setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        super(__class__, cls).tearDownClass()
        
    def get_token_for_user(self, user_id):
        return super(__class__, self).get_token_for_user(user_id)
        
    def get_token_for_author_of_thread(self, thread_id):
        return super(__class__, self).get_token_for_author_of_thread(thread_id)
        
    def test_get(self):
        token = self.get_token_for_user(2)
        response = self.client.get(
            '/users/',
            headers={"Authorization":f"Bearer {token}"}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
            
        