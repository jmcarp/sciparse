"""
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import lookup

LR = lookup.LookupRule

class Frontiers(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'publication_date',
            lambda date: csl.date_to_csl(date),
        ),
        'author' : LR(
            'author',
            lambda author: map(name.human_to_csl, author),
        ),
        'page' : LR('firstpage'),
    })
