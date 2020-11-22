from main import create_app, db
import unittest
import commands
from tests.super_test import BaseTest

class TestPosts(BaseTest, unittest.TestCase):
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
        token = self.get_token_for_user(1)
        response = self.client.get(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertTrue("posts" in data)
        
    def test_post(self):
        token = self.get_token_for_user(1)
        response = self.client.post(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"},
            json={"content":"test post"})
        self.assertEqual(response.status_code, 200)
        
        verify = self.client.get(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"}
        )
        check = verify.get_json()
        all_posts = check["posts"]
        all_content = []
        for x in all_posts:
            all_content.append(x["content"])
        self.assertTrue("test post" in all_content)
        
    def test_patch(self):
        token = self.get_token_for_user(1)
        response = self.client.put(
            '/posts/1',
            headers={"Authorization":f"Bearer {token}"},
            json={"content":"changed!"}
        )
        
        self.assertEqual(response.status_code, 200)
        
        verify = self.client.get(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"}
        )
        check = verify.get_json()
        all_posts = check["posts"]
        all_content = []
        for x in all_posts:
            all_content.append(x["content"])
        self.assertTrue("changed!" in all_content)
        
    def test_delete(self):
        token = self.get_token_for_user(1)
        response = self.client.delete(
            '/posts/2',
            headers={"Authorization":f"Bearer {token}"},
            json={"content":"changed!"}
        )
        self.assertEqual(response.status_code, 200)
        
        verify = self.client.get(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"}
        )
        
        check = verify.get_json()
        all_posts = check["posts"]
        all_content = []
        for x in all_posts:
            all_content.append(x["content"])
        self.assertTrue("delete me" not in all_content)