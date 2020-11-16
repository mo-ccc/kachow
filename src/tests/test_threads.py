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
        
        response = self.client.post('/auth/login',
                                    json={"email":"test0@test.com",
                                          "password":"123456"})
        cls.token = response.get_json()
        
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        db.create_all()
        cls.app_context.pop()
        
    def test_get(self):
        response = self.client.get('/threads/',
                                   headers={"Authorization":f"Bearer {self.token}"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
    def test_post(self):
        response = self.client.get('/threads/')
        initial = len(response.get_json())
        response = self.client.post('/threads/', 
                                    json={
                                        "author_id":0,
                                        "category_id":1,
                                        "title":"post thread",
                                        "status":1
                                    })
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/threads/11')
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title,  "post thread")
        
    def test_put(self):
        response = self.client.patch('/threads/2', 
                                   json={
                                       "category_id":1,
                                       "title":"put thread",
                                       "status":1
                                   })
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/threads/2')
        thread_title = response.get_json()["thread_info"]["title"]
        self.assertEqual(thread_title, "put thread")

    def test_delete(self):
        response = self.client.delete('/threads/1')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/threads/1')
        self.assertEqual(response.status_code, 404)
        