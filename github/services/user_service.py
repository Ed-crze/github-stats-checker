class UserService:
    def __init__(self, client):
        self.client = client

    def get_user_profile(self, username):
        try:
            return self.client.client.get(f'users/{username}')
        except Exception as e:
            print(f"Error fetching user profile: {e}")
            return None