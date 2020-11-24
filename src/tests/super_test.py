import unittest
from main import db, create_app
import commands

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
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
        if response.status_code != 200:
            print(response.data)
        
        return response.get_json()
    
    def get_token_for_author_of_thread(self, thread_id):
        token1 = self.get_token_for_user(1)
        response = self.client.get(
            f'/threads/{thread_id}',
            headers={"Authorization":f"Bearer {token1}"}
        )
        author_email = response.get_json()["thread_info"]["thread_author"]["email"]
        response = self.client.post(
            '/auth/login',
            json={
                "email":author_email,
                "password":"123456"
            }
        )
        return response.get_json()
        
    def get_token_for_admin(self):
        response = self.client.post(
            '/auth/login',
            json={
                "email":"admin@kachow.com",
                "password":"admin"
            }
        )
        
        return response.get_json()