"""
"""

# Imports
import urllib
from pyquery import PyQuery

# Project imports
import parse
from util import magic
from util import lookup
from util import htmltools

@magic.regify
class RefParse(parse.Parse):
    """ Base class for reference parsers. """
    
    def __init__(self, html, qhtml=None, **kwargs):
        
        if qhtml is None:

            # Store raw and parsed HTML
            self.html, self.source = htmltools.parse_html(html)

        else:
            
            # Memorize raw and parsed HTML
            self.html = html
            self.source = qhtml

    # Fetch class for lookups
    fetch = lookup.HTMLFetch
