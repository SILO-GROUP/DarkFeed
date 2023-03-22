from src.SiteFeed import SiteFeed

# fetches feeds from remote sources
class FeedFetcher:
    def __init__( self ):
        pass

    def fetch_source( self, source, config ):
        # fetch the content
        return SiteFeed( source, config )

    # reads from a config object
    def fetch_all_config_sources( self, config ):
        results = list()

        for feed_source in config.sites:
            results.append( self.fetch_source( feed_source, config ) )

        return results