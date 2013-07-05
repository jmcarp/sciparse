"""
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import page
from ...util import regex
from ...util import lookup

# Alias LookupRule
LR = lookup.LookupRule

class TandF(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'date',
            lambda date: csl.date_to_csl(date)
        ),
        'author' : LR(
            'creator',
            lambda creator: map(name.human_to_csl, creator)
        ),
    })

    def _parse_DOI(self):
        """ Extract article DOI. """
        
        if 'identifier' not in self.source:
            return
        
        for ident in self.source['identifier']:
            if regex.doi.match(ident):
                return ident
