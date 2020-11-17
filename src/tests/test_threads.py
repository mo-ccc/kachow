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
        
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])
        
    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        db.create_all()
        cls.app_context.pop()
        
    def test_get(self):
        response = self.client.post('/auth/login',
                                    json={"email":"test1@test.com",
                                          "password":"123456"})
        token = response.get_json()
        response = self.client.get('/threads/',
                                   headers={"Authorization":f"Bearer {token}"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
    def test_post(self):
        response = self.client.post('/auth/login',
                                    json={"email":"test1@test.com",
                                          "password":"123456"})
        token = response.get_json()
        response = self.client.post('/threads/', 
                                    json={
                                        "category_id":1,
                                        "title":"post thread",
                                        "status":1
                                    },
                                    headers={"Authorization":f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        tid = response.get_json()["thread_id"]
        response = self.client.get(f'/threads/{tid}',
                                   headers={"Authorization":f"Bearer {token}"})
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title,  "post thread")
        
    def test_put(self):
        response = self.client.post(
            '/auth/login',
            json={"email":"test1@test.com", "password":"123456"}
        )
        token = response.get_json()
        thread = self.client.get(
            '/threads/',
            headers={"Authorization":f"Bearer {token}"}
        )
        print(thread.get_json())
        author = thread.get_json()["thread_info"]["author_id"]
        response = self.client.post(
            '/auth/login',
            json={
                "email":f"test{author_id}@test.com",
                "password":"123456"
            }
        )
        token = response.get_json()
        response = self.client.patch(
            '/threads/2', 
            json={
               "category_id":1,
               "title":"put thread",
               "status":1
            },
            headers={"Authorization":f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/threads/2')
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title, "put thread")

    def test_delete(self):
        response = self.client.delete('/threads/1')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/threads/1')
        self.assertEqual(response.status_code, 404)
        