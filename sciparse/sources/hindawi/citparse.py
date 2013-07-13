"""
Citation parser for Hindawi journals.
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import misc
from ...util import name
from ...util import lookup

LR = lookup.LookupRule

class Hindawi(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'publication_date',
            lambda date: csl.date_to_csl(date)
        ),
        'author' : LR(
            'creator',
            lambda author: map(
                name.human_to_csl, 
                misc.ensure_list(author)
            )
        ),
    })
