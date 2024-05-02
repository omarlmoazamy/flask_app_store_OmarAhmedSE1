import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class BasicTests(unittest.TestCase):
    # Setup that runs before every test
    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        # Set up the in-memory database
        with app.app_context():
            db.create_all()

    # Teardown that runs after every test
    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test the home page redirect to register
    def test_home_page_redirect(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My Suit Store!', response.data)

    # Test the registration page
    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register at Suit Store', response.data)

    # Test user registration
    def test_user_registration(self):
        response = self.app.post('/register', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    # Test the login page
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to Suit Store', response.data)

    # Test user login
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
        self.assertIn(b'Welcome to My Suit Store!', response.data)

    # Test invalid user login
    def test_invalid_user_login(self):
        response = self.app.post('/login', data=dict(
            username='wronguser',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login failed. Check your credentials.', response.data)

# This allows the tests to be run from the command line
if __name__ == '__main__':
    unittest.main()
