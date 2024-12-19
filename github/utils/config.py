import os
import yaml
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self):
        self.DEFAULT_CONFIG = {
            'base_url': 'https://api.github.com',
            'username': None,
            'repo_limit': 100,
            'include_private_repos': False,
            'include_forks': True,
            'include_stars': True,
            'include_watchers': False,
            'include_overall_totals': True,
            'include_individual_totals': False,
            'timeout': 10
        }

    def load_config(self):
        with open("config.yaml", "r") as f:
            user_config = yaml.safe_load(f)
        
        config = self.DEFAULT_CONFIG.copy()
        config.update(user_config)
        
        if config['include_private_repos']:
            token = self.load_env_vars()
            if not token:
                raise Exception("GitHub access token required when include_private_repos is set to True. Please set GITHUB_ACCESS_TOKEN in .env file.")
        return config

    def load_env_vars(self):
        load_dotenv()
        return os.getenv("GITHUB_ACCESS_TOKEN")