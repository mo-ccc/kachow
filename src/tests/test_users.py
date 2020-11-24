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
        
    def get_token_for_admin(self):
        return super(__class__, self).get_token_for_admin()
        
    def test_get_users(self):
        token = self.get_token_for_user(2)
        response = self.client.get(
            '/users/',
            headers={"Authorization":f"Bearer {token}"}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
    def test_post_user(self):
        token = self.get_token_for_admin()
        response = self.client.post(
            '/users/',
            json={
                "username": "test_user6",
                "email": "test6@test.com",
                "password": "123456",
                "fname": "test",
                "lname": "test",
                "role": 2
            },
            headers={"Authorization":f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        
        login = self.get_token_for_user(6)
        
        test = self.client.get(
            '/threads/',
            headers={"Authorization":f"Bearer {login}"}
        )
        self.assertEqual(test.status_code, 200)
        
    def test_put_user(self):
        token = self.get_token_for_admin()
        response = self.client.put(
            '/users/4',
            json={
                "username": "put_user",
            },
            headers={"Authorization":f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        
    def test_delete_user(self):
        token = self.get_token_for_admin()
        response = self.client.delete(
            '/users/3',
            headers={"Authorization":f"Bearer {token}"}
        )
        print(response.data)
        
        self.assertEqual(response.status_code, 200)
        
        verify = self.get_token_for_user(2)
        print(verify)
            