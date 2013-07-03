"""
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import page
from ...util import lookup

LR = lookup.LookupRule

class Pubmed(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'date',
            lambda date: csl.date_to_csl(date)
        ),
        'author' : LR(
            'authors',
            lambda author: map(name.human_to_csl, author.split(', '))
        ),
    })

    def _parse_pages(self):
        """ Extract page range. """
        
        return page.fetch_pages(self, 'firstpage', 'lastpage')
