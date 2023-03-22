import configparser
import re
from src.FeedSource import FeedSource

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
                self.cache_dir = config.get( 'main', 'cache_dir' )
            else:
                tags_processed = config.get( section_name, 'tags' )
                self.sites.append(
                    FeedSource(
                        feed_url=config.get(section_name, 'url'),
                        title=section_name,
                        tags=re.split( r',\s*|\s+', tags_processed ),
                        tag_filter=config.getboolean( section_name, 'tag_filter' )
                    )
                )

    def get_site_by_uid(self, uid ):
        for site in self.sites:
            if site.uid == uid:
                return site