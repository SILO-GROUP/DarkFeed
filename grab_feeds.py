import feedparser
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from time import mktime
import configparser
import re


class Source:
    def __init__( self, title, url, tags ):
        self.title = title
        self.url = url
        self.tags = tags


class Config:
    def __init__( self, filename ):
        config = configparser.ConfigParser()
        config.read(filename)
        self.sites = list()
        for section_name in config.sections():
            if section_name == "main":
                self.site_name = config.get( 'main', 'site_name' )
                self.theme = config.get( 'main', 'theme' )
                self.subtitle = config.get( 'main', 'subtitle' )
            else:
                tags_processed = config.get( section_name, 'tags' )
                self.sites.append(
                    Source(
                        url=config.get(section_name, 'url'),
                        title=section_name,
                        tags=re.split( r',\s*|\s+', tags_processed )
                    )
                )


class Article:
    def __init__(self, parent_title, entry, config ):
        self.config = config
        self.parent_blog = parent_title
        self.title = entry['title']
        self.author = entry['author']
        self.summary = entry['summary']
        self.content = entry['content'][0]['value']
        self.url = entry['link']

        self._date_raw = entry['published_parsed']
        self._datetime_obj = datetime.fromtimestamp(mktime(self._date_raw))
        self.date = self._datetime_obj.strftime('%Y-%m-%d')

        self.tags = list()
        self._tags_raw = entry['tags']
        for raw_tag in self._tags_raw:
            self.tags.append(raw_tag['term'])


# WPSiteFeed is a python object representing the feed results for one site
class WPSiteFeed:
    def __init__( self, url, listen_tags, blog_title, config ):
        self.config = config
        feed_result = feedparser.parse( url )
        self.title = blog_title
        self.subtitle = feed_result['feed']['subtitle']
        self.site_url = feed_result['feed']['link']
        self.feed_url = feed_result['feed']['links'][0]['href']
        self.listen_tags = listen_tags

        self._entries_raw = feed_result['entries']
        self.entries = list()
        for entry in self._entries_raw:
            article = Article( self.title, entry, self.config )
            if any( x in self.listen_tags for x in article.tags ):
                self.entries.append( article )


class SiteGenerator:
    def __init__( self, config ):
        self.config = config
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join( self.project_root, 'themes' )
        self.theme_dir = os.path.join( self.templates_dir, self.config.theme )
        self.env = Environment( loader = FileSystemLoader( self.theme_dir ))
        self.output_dir = os.path.join( self.project_root, 'output' )

    def generate_site(self):
        index_template = self.env.get_template( 'index.html.j2' )
        index_output = os.path.join( self.output_dir, 'index.html' )

        # fetch the feeds and deserialize
        site_feeds = list()
        for source in self.config.sites:
            site_feeds.append(
                WPSiteFeed(
                    source.url,
                    listen_tags=source.tags,
                    blog_title=source.title,
                    config=self.config
                )
            )

        unsorted_entries = list()
        for result in site_feeds:
            unsorted_entries.extend( result.entries )
        sorted_entries = sorted( unsorted_entries, key=lambda x: x._datetime_obj, reverse=True )

        with open( index_output, 'w' ) as index_fh:
            index_fh.write(
                index_template.render(
                    config = self.config,
                    site_feeds = site_feeds,
                    entries = sorted_entries
                )
            )


def main():
    config = Config( 'config.ini' )

    site_controller = SiteGenerator( config )
    site_controller.generate_site()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

