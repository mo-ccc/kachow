import unittest
from main import create_app, db
import commands

class test_endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.drop_all()
        db.create_all()
        
        # invokes 'flask db seed' in console
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])
        
    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        db.create_all()
        cls.app_context.pop()
        
    def get_token_for_user(self, user_id):
        response = self.client.post(
            '/auth/login',
            json={
                "email":f"test{user_id}@test.com",
                "password":"123456"
            }
        )
        return response.get_json()
    
    def get_token_for_author_of_thread(self, thread_id):
        token1 = self.get_token_for_user(1)
        response = self.client.get(
            f'/threads/{thread_id}',
            headers={"Authorization":f"Bearer {token1}"}
        )
        author_id = response.get_json()["thread_info"]["author_id"]
        return self.get_token_for_user(author_id)
        
    def test_get(self):
        token = self.get_token_for_user(1)
        response = self.client.get(
            '/threads/',
            headers={"Authorization":f"Bearer {token}"}
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
    def test_post(self):
        token = self.get_token_for_user(1)
        response = self.client.post(
            '/threads/', 
            json={
                "category_id":1,
                "title":"post thread",
                "status":1
            },
            headers={"Authorization":f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        
        thread_id = response.get_json()["thread_id"]
        response = self.client.get(
            f'/threads/{thread_id}',
            headers={"Authorization":f"Bearer {token}"}
        )
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title,  "post thread")
        
    def test_put(self):
        token1 = self.get_token_for_user(1)
        token2 = self.get_token_for_author_of_thread(2)
        response = self.client.put(
            '/threads/2', 
            json={
               "category_id":1,
               "title":"put thread",
               "status":1
            },
            headers={"Authorization":f"Bearer {token2}"}
        )
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(
            '/threads/2',
            headers={"Authorization":f"Bearer {token1}"}
        )
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title, "put thread")

    def test_delete(self):
        token = self.get_token_for_author_of_thread(1)
        response = self.client.delete(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            '/threads/1',
            headers={"Authorization":f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 404)
        