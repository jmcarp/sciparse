"""
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import lookup

# Alias LookupRule
LR = lookup.LookupRule

class Nature(citparse.CitParse):
    
    # Copy superclass lookups and update
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'date',
            lambda date: csl.date_to_csl(date)
        ),
        'author' : LR(
            'authors',
            lambda authors: map(name.human_to_csl, authors.split('; '))
        ),
    })
