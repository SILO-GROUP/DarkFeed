import os
from jinja2 import Environment, FileSystemLoader

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
