from github.core.main import GitHubCrawler

class Run:
    def __init__(self):
        self.crawler = GitHubCrawler()
    
    def execute(self):
        return self.crawler.crawl()

crawl = Run().execute