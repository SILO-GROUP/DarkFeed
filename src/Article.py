from datetime import datetime
from time import mktime
import re
import hashlib

class Article:
    def __init__(self, entry, parent_uid, config ):
        self._raw_entry = entry
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

        self.uid = self.content_hash()
        self.parent_uid = parent_uid
        self.parent = config.get_site_by_uid( self.parent_uid )

    def content_hash(self):
        sha1 = hashlib.sha1()
        sha1.update(self.url.encode('utf-8'))
        return sha1.hexdigest()


    def __json_encode__(self):
        return {
            'url': self.url,
            'is_commit_feed': self.is_commit_feed,
            'title': self.title,
            'author': self.author,
            'summary': self.summary,
            'content': self.content,
            'date': self.date,
            'tags': self.tags,
            'uid': self.uid,
            'parent_uid': self.parent_uid
        }

    @classmethod
    def __json_decode__(cls, data, config ):
        entry = {
            'link': data['url'],
            'title': data['title'],
            'author': data['author'],
            'summary': data['summary'],
            'content': [{'value': data['content']}],
            'published_parsed': datetime.strptime(data['date'], '%Y-%m-%d').timetuple(),
            'tags': [{'term': tag} for tag in data['tags']] if data['tags'] else [],
            'parent_uid': data['parent_uid']
        }
        return cls( entry, data['parent_uid'], config )