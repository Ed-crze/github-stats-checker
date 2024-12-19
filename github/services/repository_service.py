class RepositoryService:
    def __init__(self, client):
        self.client = client
        self.config = client.config

    def get_user_repositories(self, username):
        repos = []
        page = 1
        
        while True:
            params = {
                'page': page,
                'per_page': self.config['repo_limit'],
                'type': 'all' if self.config['include_private_repos'] else 'public'
            }
            
            try:
                # Use /user/repos endpoint for authenticated user to get private repos
                endpoint = 'user/repos' if self.config['include_private_repos'] else f'users/{username}/repos'
                page_repos = self.client.client.get(endpoint, params=params)
            except Exception as e:
                print(f"Error fetching repositories: {e}")
                break
                
            if not page_repos:
                break
                
            filtered_repos = []
            for repo in page_repos:
                if not self.config['include_stars'] and repo['stargazers_count'] == 0:
                    continue
                if not self.config['include_forks'] and repo['fork']:
                    continue
                if not self.config['include_watchers'] and repo['watchers_count'] == 0:
                    continue
                if not self.config['include_private_repos'] and repo['private']:
                    continue
                filtered_repos.append(repo)
            
            repos.extend(filtered_repos)
            page += 1
            
            if len(repos) >= self.config['repo_limit']:
                repos = repos[:self.config['repo_limit']]
                break
                
        return repos

    def get_repository_stats(self, username):
        if not self.config['include_overall_totals'] and not self.config['include_individual_totals']:
            raise Exception("At least one of include_overall_totals or include_individual_totals must be True")
            
        repos = self.get_user_repositories(username)
        
        if not repos:
            return None
            
        stats = {}
        
        if self.config['include_overall_totals']:
            stats.update(self._calculate_overall_stats(repos))
            
        if self.config['include_individual_totals']:
            stats.update(self._calculate_individual_stats(repos))
        
        self._print_repository_details(stats)
        return stats

    def _calculate_overall_stats(self, repos):
        stats = {
            'overall_stats': {
                'total_repos': len(repos),
                'public_repos': sum(1 for repo in repos if not repo['private'])
            }
        }
        
        if self.config['include_private_repos']:
            stats['overall_stats']['private_repos'] = sum(1 for repo in repos if repo['private'])
            
        if self.config['include_stars']:
            stats['overall_stats']['total_stars'] = sum(repo['stargazers_count'] for repo in repos)
            
        if self.config['include_forks']:
            stats['overall_stats']['total_forks'] = sum(repo['forks_count'] for repo in repos)
        
        if self.config['include_watchers']:
            stats['overall_stats']['total_watchers'] = sum(repo['watchers_count'] for repo in repos)
            
        return stats

    def _calculate_individual_stats(self, repos):
        repo_stats = []
        
        for repo in repos:
            repo_info = {
                'name': repo['name'],
                'visibility': 'Public' if not repo['private'] else 'Private',
                'language': repo['language'],
                'updated_at': repo['updated_at'],
                'description': repo['description']
            }
            
            if self.config['include_stars']:
                repo_info['stars'] = repo['stargazers_count']

            if self.config['include_forks']:
                repo_info['forks'] = repo['forks_count']

            if self.config['include_watchers']:
                repo_info['watchers'] = repo['watchers_count']
                
            repo_stats.append(repo_info)
            
        return {'repositories': repo_stats}

    def _print_repository_details(self, stats):
        if self.config['include_overall_totals'] and 'overall_stats' in stats:
            overall = stats['overall_stats']
            print("\nOverall Statistics:")
            print(f"Total Repositories: {overall['total_repos']}")
            print(f"Public Repositories: {overall['public_repos']}")
            
            if self.config['include_private_repos']:
                print(f"Private Repositories: {overall.get('private_repos', 0)}")
            
            if self.config['include_stars']:
                print(f"Total Stars: {overall.get('total_stars', 0)}")

            if self.config['include_forks']:
                print(f"Total Forks: {overall.get('total_forks', 0)}")
            
            if self.config['include_watchers']:
                print(f"Total Watchers: {overall.get('total_watchers', 0)}")
                
        if self.config['include_individual_totals'] and 'repositories' in stats:
            print("\nIndividual Repository Statistics:")
            for repo in stats['repositories']:
                print(f"\nRepository: {repo['name']}")
                print(f"{repo['visibility']}")
                print(f"Language: {repo['language'] or 'Not specified'}")
                
                if self.config['include_stars']:
                    print(f"Stars: {repo.get('stars', 0)}")

                if self.config['include_forks']:
                    print(f"Forks: {repo['forks']}")
                    
                if self.config['include_watchers']:
                    print(f"Watchers: {repo.get('watchers', 0)}")
                    
                if repo['description']:
                    print(f"Description: {repo['description']}")