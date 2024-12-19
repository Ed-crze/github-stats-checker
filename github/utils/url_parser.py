from urllib.parse import urlparse

class URLParser:
    def __init__(self):
        self.url = None

    def extract_username_from_url(self, url):
        self.url = url
        try:
            parsed = urlparse(self.url)
            path_parts = parsed.path.strip('/').split('/')
            return path_parts[0] if path_parts else None
        except Exception:
            return None