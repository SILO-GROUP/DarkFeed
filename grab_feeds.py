#!/usr/bin/env python3
from src.Config import Config
from src.SiteGenerator import SiteGenerator





def main():
    config = Config( 'config.ini' )
    site_controller = SiteGenerator( config )
    site_controller.generate_site()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

