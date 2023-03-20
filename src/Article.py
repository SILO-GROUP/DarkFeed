from datetime import datetime
from time import mktime
import re

class Article:
    def __init__(self, parent_title, entry, config ):
        self.config = config
        self.parent_blog = parent_title
        self.url = entry['link']

        if self.url.startswith("https://github.com"):
            self.is_commit_feed = True
        else:
            self.is_commit_feed = False

        if self.is_commit_feed:
            self.title = re.split('\/', self.url)[-1]
        else:
            self.title = entry['title']
        self.author = entry['author']
        self.summary = entry['summary']
        self.content = entry['content'][0]['value']

        try:
            self._date_raw = entry['published_parsed']
        except KeyError:
            self._date_raw = entry['updated_parsed']
        self._datetime_obj = datetime.fromtimestamp(mktime(self._date_raw))
        self.date = self._datetime_obj.strftime('%Y-%m-%d')

        self.tags = list()
        if not self.is_commit_feed:
            self._tags_raw = entry['tags']
            for raw_tag in self._tags_raw:
                self.tags.append(raw_tag['term'])
        else:
            self.tags = None
