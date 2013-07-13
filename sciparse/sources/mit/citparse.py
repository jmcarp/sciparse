"""
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import regex
from ...util import lookup

LR = lookup.LookupRule

class MIT(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'date',
            lambda date: csl.date_to_csl(date)
        ),
        'author' : LR(
            'creator',
            lambda author: map(name.human_to_csl, author)
        ),
    })
    
    def _parse_doi(self):
        
        for ident in self.source['identifier']:
            if regex.doi.match(ident):
                return ident
