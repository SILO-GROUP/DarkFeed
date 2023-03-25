import hashlib

class FeedSource:
    def __init__( self, title, feed_url, tags, tag_filter ):
        self.title = title
        self.url = feed_url
        print("FEED URL: '{0}'.".format(self.url))
        self.tags = tags
        self.tag_filter = tag_filter
        self.uid = self.site_hash()
        print("FEED UID: '{0}'.\n".format(self.uid))

    def site_hash(self):
        sha1 = hashlib.sha1()
        sha1.update(self.url.encode('utf-8'))
        return sha1.hexdigest()