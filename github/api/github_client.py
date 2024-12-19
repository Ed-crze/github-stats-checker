from github.http.client import HTTPClient

class GitHubClient:
    def __init__(self, config=None, token=None):
        self.config = config
        self.headers = {}
        
        if token:
            self.headers.update({
                'Authorization': f'Bearer {token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        else:
            self.headers.update({
                'Accept': 'application/vnd.github.v3+json'
            })
            
        self.client = HTTPClient(
            config['base_url'], 
            self.headers,
            timeout=config['timeout']
        )