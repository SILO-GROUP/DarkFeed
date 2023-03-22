import os
from jinja2 import Environment, FileSystemLoader
from src.SiteFeed import SiteFeed

def get_nth_parent_directory_path(n):
    current_file_path = os.path.realpath(__file__)
    for i in range(n):
        current_file_path = os.path.dirname(current_file_path)
    parent_directory_path = os.path.abspath(current_file_path)
    return parent_directory_path

class SiteGenerator:
    def __init__( self, config ):
        self.config = config
        self.project_root = get_nth_parent_directory_path(2)
        self.templates_dir = os.path.join( self.project_root, 'themes' )
        self.theme_dir = os.path.join( self.templates_dir, self.config.theme )
        self.env = Environment( loader = FileSystemLoader( self.theme_dir ))
        self.output_dir = os.path.join( self.project_root, 'output' )

    def generate_site(self, feeds):
        index_template = self.env.get_template( 'index.html.j2' )
        index_output = os.path.join( self.output_dir, 'index.html' )

        unsorted_entries = list()
        for result in feeds:
            unsorted_entries.extend( result.entries )
        sorted_entries = sorted(
            unsorted_entries,
            key=lambda x: x._datetime_obj,
            reverse=True
        )

        with open( index_output, 'w' ) as index_fh:
            index_fh.write(
                index_template.render(
                    config = self.config,
                    site_feeds = feeds,
                    entries = sorted_entries
                )
            )
