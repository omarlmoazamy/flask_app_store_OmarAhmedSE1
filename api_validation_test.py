import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class APIValidationTestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app to use the testing database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Create the database and the tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all the tables in the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        # Simulate a POST request to create a new user
        response = self.app.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirection after registration

        # Verify the user was created in the database
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)
            self.assertTrue(user.check_password('newpassword'))

    def test_user_login(self):
        # Create a user
        with app.app_context():
            hashed_password = generate_password_hash('testpassword', method='pbkdf2:sha256')
            user = User(username='testuser', email='testuser@example.com', password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()

        # Simulate a POST request to log in the user
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirection after login

    # Additional tests can be added here

if __name__ == '__main__':
    unittest.main()
