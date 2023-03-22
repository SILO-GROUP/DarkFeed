# DarkFeed

DarkFeed is a minimalist, fully themeable PlanetPlanet clone written in Python3.  It's an RSS aggregator that takes a list of feed URLs and generates an aggregated content view in static html.

DarkFeed wasn't designed to be written well, it was designed to be implemented quickly, so, if you have improvements, pull requests are welcome.

# Instructions

First, clone the repo to your desired location.

## Set up config.ini
1. Set up the site details for the website you're creating, such as site_name and theme, subtitle
2. Set the cache directory to where you want the files to be generated.  htdocs is inadvisable for security reasons.
3. Set the RSS feeds you want to monitor.
4. Set the tags you want if you want to filter by tags.

## use the tools directory
In `tools/` you'll see two files:
 - generate_site
 - update_caches

They do what they look like they do.


Set a cron to execute at your desired update frequency
