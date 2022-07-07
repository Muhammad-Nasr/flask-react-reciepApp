import unittest
from main import db, create_app
from config import TestConfig

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(self)
        

    def test_signup_and_login(self):
        data = {
            "username": "ali",
            "email": "ali@email.com",
            "password": "cat"
            }
        signup_resp = self.client.post('/auth/signup', json=data)
        self.assertEqual(signup_resp.status_code, 201)

        login_resp = self.client.post('auth/login',
        json={"email": "ali@email.com",
            "password": "cat"})
        self.assertEqual(login_resp.status_code, 200)

    def test_create_recipe(self):
        data = {
            "username": "ali",
            "email": "ali@email.com",
            "password": "cat"
            }
        signup_resp = self.client.post('/auth/signup', json=data)
        login_resp = self.client.post('auth/login',
        json={"email": "ali@email.com",
            "password": "cat"})
        
        acess_token = login_resp.json['access_token']
        new_recipe = self.client.post('/recipe/recipes', 
                json={"title":"test_recipe","description":"my first test recipe"},
                headers={
                    "Authorization":f"Bearer {acess_token}"
                })
        self.assertEqual(new_recipe.status_code, 201)

    def test_get_all_recipes(self):
        all_recipes = self.client.get('/recipe/recipes')
        print(all_recipes.json)
        self.assertTrue('test_recipe' in all_recipes.json)
        
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
