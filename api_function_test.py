import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class APITestCase(unittest.TestCase):
    # Set up a test database
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_store.db'  # Updated to test_store.db
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    # Tear down the test database
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test the registration functionality
    def test_register_function(self):
        # Create a new user
        with app.app_context():
            hashed_password = generate_password_hash('testpassword', method='pbkdf2:sha256')
            new_user = User(username='testuser', email='testuser@example.com', password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()

        # Verify that the user was created
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')

    # Test the login functionality
    def test_login_function(self):
        # First, create a user using the registration test
        self.test_register_function()

        # Attempt to log in with the correct credentials
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to the home page

        # Attempt to log in with incorrect credentials
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should return to the login page

    # Add more test cases as needed for other functionalities

if __name__ == '__main__':
    unittest.main()
