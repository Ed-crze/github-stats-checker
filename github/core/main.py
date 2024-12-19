from github.api.github_client import GitHubClient
from github.services.auth_service import AuthService
from github.services.repository_service import RepositoryService
from github.services.user_service import UserService
from github.utils.config import ConfigLoader
from github.utils.url_parser import URLParser

class GitHubCrawler:
    def __init__(self):
        self.config_loader = ConfigLoader()
        self.config = self.config_loader.load_config()
        self.token = self.config_loader.load_env_vars()
        
        self.client = GitHubClient(self.config, self.token)
        self.auth_service = AuthService(self.client)
        self.repo_service = RepositoryService(self.client)
        self.user_service = UserService(self.client)
        self.url_parser = URLParser()

    def crawl(self):
        username = self.config["username"]
        
        if 'github.com/' in username:
            parsed_username = self.url_parser.extract_username_from_url(username)
            if parsed_username:
                username = parsed_username
        
        if self.token:
            auth_status = self.auth_service.check_token_permissions()
            if not auth_status and self.config['include_private_repos']:
                raise Exception("Failed to verify token permissions for private repository access")
        
        user_profile = self.user_service.get_user_profile(username)
        if not user_profile:
            raise Exception(f"Failed to fetch profile for user: {username}")
        
        repo_stats = self.repo_service.get_repository_stats(username)
        if not repo_stats:
            raise Exception(f"Failed to fetch repository statistics for user: {username}")
        
        return {
            'user_profile': user_profile,
            'repository_stats': repo_stats
        }