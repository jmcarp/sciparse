"""
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import lookup

LR = lookup.LookupRule

class Wiley(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'publication_date',
            lambda date: csl.date_to_csl(date)
        ),
    })
    
    fpage_key = 'firstpage'
    lpage_key = 'lastpage'

    def _parse_author(self):
        """ Extract authors from citation. """
        
        # Quit if no author
        if 'author' not in self.source:
            return
        
        # Extract CSL-formatted name for each author
        return map(name.human_to_csl, self.source['author'])
