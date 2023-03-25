import feedparser
from src.Article import Article
import hashlib

# WPSiteFeed is a python object representing the feed results for one site
# Remote Interaction Happens Here
class SiteFeed:
    def __init__( self, feed_source, config ):
        self.config = config

        # fetch and parse feed
        feed_result = feedparser.parse(feed_source.url)
        try:
            self.subtitle = feed_result['feed']['subtitle']
        except KeyError:
            self.subtitle = ""
        self.site_url = feed_result['feed']['link']
        self.url = feed_result['feed']['links'][0]['href']
        self.filter_by_tags = feed_source.tag_filter
        if self.filter_by_tags:
            self.listen_tags = feed_source.tags

        self._entries_raw = feed_result['entries']

        # create a uid for caching purposes
        # should be based on URL so that updates to URLs update content
        self.uid = feed_source.uid

        # grab articles from the raw results, convert them to
        # Articles, and append them to self.entries[]
        self.entries = self.sift_entries()


        self.title = feed_source.title

    def sift_entries(self):
        entries = list()
        for entry in self._entries_raw:
            article = Article( entry, self.uid, self.config, parent=self )
            if article.is_commit_feed:
                entries.append( article )
            else:
                if self.filter_by_tags:
                    if any( x in self.listen_tags for x in article.tags ):
                        entries.append( article )
                else:
                    entries.append( article )
        return entries

    def __json_encode__(self):
        return {
            'subtitle': self.subtitle,
            'site_url': self.site_url,
            'uid': self.uid,
        }

    # we override some values based on config for templating
    @classmethod
    def __json_decode__(cls, filedata, config ):
        site_feed = cls( config.get_site_by_uid( filedata['uid'] ), config )
        site_feed.subtitle = filedata['subtitle']
        site_feed.site_url = filedata['site_url']
        site_feed.uid = filedata['uid']

        return site_feed