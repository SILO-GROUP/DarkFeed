import feedparser
from src.Article import Article

# WPSiteFeed is a python object representing the feed results for one site
class WPSiteFeed:
    def __init__( self, url, listen_tags, blog_title, config ):
        self.config = config
        feed_result = feedparser.parse( url )
        self.title = blog_title
        try:
            self.subtitle = feed_result['feed']['subtitle']
        except KeyError:
            self.subtitle = None
        self.site_url = feed_result['feed']['link']
        self.feed_url = feed_result['feed']['links'][0]['href']
        self.listen_tags = listen_tags

        self._entries_raw = feed_result['entries']
        self.entries = list()
        for entry in self._entries_raw:
            article = Article( self.title, entry, self.config )
            if article.is_commit_feed:
                self.entries.append( article )
            else:
                if any( x in self.listen_tags for x in article.tags ):
                    self.entries.append( article )
