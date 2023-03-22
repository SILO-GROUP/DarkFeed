import os
import json
from pathlib import Path
from src.SiteFeed import SiteFeed
from src.Article import Article

# Controller for Cache
class CacheIO:
    def __init__( self, config ):
        self.cache_root_dir = os.path.abspath( config.cache_dir )
        self.config = config

    def _dir_contents(self, dir_path ):
        try:
            if not os.path.isdir(dir_path):
                raise ValueError( "The path provided sucks: '{0}'.  Expected a directory.".format( dir_path ) )
            directory_contents = os.listdir(dir_path)
            return directory_contents

        except Exception as e:
            print( "Error: {0}".format( e ) )
            return None

    # write to cache
    def write_article( self, site_cache_dir, entry ):
        entryStr = json.dumps( entry, default=lambda a: a.__json_encode__(), indent=4 )

        # write serialized entry to file named after the entry uid
        with open(os.path.join( site_cache_dir, entry.uid ), "wt") as fh:
            fh.write(entryStr)
            print("\tCaching article '{0}' ('{1}').".format(entry.uid, entry.title))

    # write a site to cache, including its entries
    # should be designed to map articles to parent site uid while still allowing config during
    # site generation to override site properties mapped to uid, which is derived from url
    def write_site(self, site_feed ):
        site_entries = site_feed.entries
        site_cache_dir = Path ( os.path.join( self.cache_root_dir, site_feed.uid ) )
        print("Caching site '{0}' ('{1}', '{2}').".format(site_feed.uid, site_feed.title, site_feed.feed_url))
        # create full directory path for cache directory root if it doesn't exist
        # create a subdir that matches the site's UID (unique by url)
        site_cache_dir.mkdir( parents=True, exist_ok=True )

        # create a file of the same uid in that dir to contain the site feed metadata
        with open( os.path.join( site_cache_dir, site_feed.uid ), "wt" ) as sitefh:
            siteStr = json.dumps( site_feed, default=lambda a: a.__json_encode__(), indent=4 )
            sitefh.write( siteStr )

        # iterate through entries:
        for entry in site_entries:
            # write them to cache
            self.write_article( site_cache_dir, entry )

    # write a list of site_feeds to cache
    def write_all( self, site_feeds ):
        for site_feed in site_feeds:
            self.write_site( site_feed )

    def read_article( self, file_path ):
        with open( file_path, 'r' ) as json_file:
            json_data = json_file.read()
        article_data = json.loads(json_data)
        article = Article.__json_decode__(article_data, self.config)
        return article

    def _is_site( self, file_path ):
        basename = os.path.basename( file_path )
        dirname = os.path.dirname( file_path )
        parent_dir_basename = os.path.basename( dirname )
        return basename == parent_dir_basename


    # walk through cache dir
    def read_articles(self, site_cache_dir  ):
        article_uids = self._dir_contents( site_cache_dir )

        articles_obj = list()
        for uid in article_uids:
            article_cache_file = os.path.join(site_cache_dir, uid)
            if not self._is_site( article_cache_file):
                article = self.read_article( article_cache_file )
                articles_obj.append( article )
        return articles_obj

    def read_site( self, site_uid ):
        site_cache_dir = Path ( os.path.join( self.cache_root_dir, site_uid ) )
        site_cache_file = os.path.join( site_cache_dir, site_uid )
        with open(site_cache_file, 'r') as json_file:
            json_data = json_file.read()

        site_feed_data = json.loads(json_data)
        site_feed = SiteFeed.__json_decode__(site_feed_data, self.config)

        # we now have the site loaded up in site_feed
        articles = self.read_articles( site_cache_dir )

        # append as entries property to site feed
        site_feed.entries = articles


        return site_feed

    def read_all_sites(self):
        site_uids = self._dir_contents( self.cache_root_dir )
        sites_obj = list()

        for uid in site_uids:
            site = self.read_site( uid )
            sites_obj.append(site)
        # all sites and their entries:
        return sites_obj



