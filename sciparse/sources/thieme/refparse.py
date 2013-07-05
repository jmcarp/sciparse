"""
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import csl
from ...util import name
from ...util import regex
from ...util import lookup

# Alias LookupRule
LR = lookup.LookupRule

class Thieme(refparse.RefParse):
    
    lookups = {
        'title' : LR('a[href^="/ejournals/linkout/"]')
    }
    
    def _parse_author(self):
        """ Extract authors from reference. """
        
        # Copy text
        text = self.source.text()
        
        # Ensure reference number in text
        ref_num = self.source('strong').text()
        if not ref_num or ref_num not in text:
            return
        
        # Ensure reference title in text
        if 'title' not in self.data or self.data['title'] not in text:
            return
        
        # Extract text between reference number and reference title
        text = text[text.index(ref_num) + len(ref_num):]
        text = text[:text.index(self.data['title'])]
        text = text.strip()

        return [name.human_to_csl(author) for author in text.split(',')]

    doi_pattern = re.compile(r'/ejournals/linkout/(.*?)/id', re.I)
    def _parse_DOI(self):
        
        # Find DOI link
        doi_link = self.source('a[href^="/ejournals/linkout/"]')

        # Quit if no DOI link found
        if not doi_link:
            return

        doi_match = self.doi_pattern.search(doi_link.attr('href'))
        if doi_match:
            return doi_match.groups()[0]
        
        # Compare link against DOI pattern
        doi_match = regex.doi.search(self.html)
        if doi_match:
            return doi_match.groups()[0]
