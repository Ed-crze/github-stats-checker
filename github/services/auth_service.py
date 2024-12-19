class AuthService:
    def __init__(self, client):
        self.client = client

    def check_token_permissions(self):
        try:
            response = self.client.client.get('user')

            return {
                'user_info': response,
                'scopes': self.client.client.headers.get('X-OAuth-Scopes', '').split(', ')
            }
        except Exception as e:
            if self.client.headers.get('Authorization') is None:
                print("No GitHub token provided. Private repositories will not be accessible.")
                return None
            print(f"Error checking token permissions: {e}")
            return None