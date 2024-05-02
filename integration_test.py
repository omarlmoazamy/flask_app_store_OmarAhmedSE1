import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class IntegrationTests(unittest.TestCase):
    # Setup that runs before every test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    # Teardown that runs after every test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test registration functionality
    def test_user_registration(self):
        response = self.app.post('/register', data=dict(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in.', response.data)

    # Test login functionality
    def test_user_login(self):
        # Create a user
        hashed_password = generate_password_hash('testpassword', method='pbkdf2:sha256')
        user = User(username='testuser', email='testuser@example.com', password_hash=hashed_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        # Attempt to login
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    # Test home page access after login
    def test_home_access_after_login(self):
        # Create and login a user
        self.test_user_login()

        # Access home page
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My Suit Store!', response.data)

if __name__ == '__main__':
    unittest.main()
