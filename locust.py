from locust import HttpUser, task, between
import uuid

class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def register(self):
        # Generate a unique username and email for each request
        unique_id = str(uuid.uuid4())
        username = f'user_{unique_id}'
        email = f'{username}@example.com'
        password = 'password'

        # Post request to the register endpoint
        self.client.post("/register", {
            "username": username,
            "email": email,
            "password": password
        })

    @task
    def login(self):
        # Use a predefined user for login
        self.client.post("/login", {
            "username": "testuser",
            "password": "testpassword"
        })

    @task
    def home(self):
        # Access the home page
        self.client.get("/home")

# Additional tasks can be added to simulate user behavior
