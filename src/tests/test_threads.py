import unittest
from main import create_app, db
from tests.super_test import BaseTest
import commands

class test_endpoints(BaseTest, unittest.TestCase):
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
        
    def test_get_thread(self):
        token = self.get_token_for_user(2)
        response = self.client.get(
            '/threads/',
            headers={"Authorization":f"Bearer {token}"}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
    def test_post_thread(self):
        token = self.get_token_for_user(2)
        response = self.client.post(
            '/threads/', 
            json={
                "categories":[1, 2],
                "title":"post thread",
                "status":1
            },
            headers={"Authorization":f"Bearer {token}"}
        )
        if response.status_code != 200:
            print(response.data)
        self.assertEqual(response.status_code, 200)
        
        thread_id = response.get_json()["thread_id"]
        response = self.client.get(
            f'/threads/{thread_id}',
            headers={"Authorization":f"Bearer {token}"}
        )
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title,  "post thread")
        
    def test_put_thread(self):
        token1 = self.get_token_for_user(3)
        token2 = self.get_token_for_author_of_thread(2)
        response = self.client.put(
            '/threads/2', 
            json={
               "categories":[1, 2],
               "title":"put thread",
               "status":1
            },
            headers={"Authorization":f"Bearer {token2}"}
        )
        if response.status_code != 200:
            print(response.data)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(
            '/threads/2',
            headers={"Authorization":f"Bearer {token1}"}
        )
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title, "put thread")

    def test_delete_thread(self):
        token = self.get_token_for_author_of_thread(1)
        response = self.client.delete(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"}
        )
        if response.status_code != 400:
            print(response.data)
        self.assertEqual(response.status_code, 400)

        