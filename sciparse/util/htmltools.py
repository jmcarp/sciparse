"""
"""

# Imports
import urllib
from pyquery import PyQuery

#

def parse_html(html):
    """

    :param html:

    """

    # Unquote HTML (fixes occasional problems w/ DOIs)
    html = urllib.unquote(html)

    # Parse HTML using PyQuery
    qhtml = PyQuery(html)
    
    # Return results
    return html, qhtml

def parse_link(qhtml, link_selector, pattern):
    """

    :param qhtml:
    :param link_selector:
    :param pattern:

    """
    # Get links
    links = qhtml(link_selector)
    
    # Iterate over links until found
    for link in links:
        match = pattern.search(link.get('href', ''))
        if match:
            return match.groups()[0] 
