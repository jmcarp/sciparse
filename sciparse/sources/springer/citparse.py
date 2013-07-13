"""
Citation parser for Springer journals.
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import regex
from ...util import lookup

LR = lookup.LookupRule

class Springer(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'author' : LR(
            'author',
            lambda author: map(name.human_to_csl, author)
        ),
    })
