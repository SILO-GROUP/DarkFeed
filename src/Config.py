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
            else:
                tags_processed = config.get( section_name, 'tags' )
                self.sites.append(
                    FeedSource(
                        url=config.get(section_name, 'url'),
                        title=section_name,
                        tags=re.split( r',\s*|\s+', tags_processed )
                    )
                )
