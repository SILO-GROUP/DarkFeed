#!/usr/bin/env python3
from src.Config import Config
from src.CacheIO import CacheIO
from src.SiteGenerator import SiteGenerator

# fetch sites
# cache them

def main():
    config = Config( 'config.ini' )

    # writes to and reads from filesystem cache
    cache_controller = CacheIO( config )

    # writes all fetched feeds to filesystem
    feeds = cache_controller.read_all_sites()

    site_generator = SiteGenerator( config )

    # generate the site from the cached feeds
    site_generator.generate_site( feeds )

    print("Completed regenerating site.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

