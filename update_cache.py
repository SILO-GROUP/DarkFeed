#!/usr/bin/env python3
from src.Config import Config
from src.FeedFetcher import FeedFetcher
from src.CacheIO import CacheIO

# fetch sites
# cache them

def main():
    config = Config( 'config.ini' )

    # gets feeds
    feed_fetcher = FeedFetcher()

    # writes to and reads from filesystem cache
    cache_controller = CacheIO( config )

    # fetches all feeds listed in config object to variable
    site_feeds = feed_fetcher.fetch_all_config_sources( config )

    # writes all fetched feeds to filesystem
    cache_controller.write_all( site_feeds )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

