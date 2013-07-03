"""
"""

# Imports
import json

# Project imports
import parse
from util import misc
from util import magic
from util import lookup
from util import jsontools

LR = lookup.LookupRule

@magic.regify
class CitParse(parse.Parse):
    
    def __init__(self, data):
        """ Initialize and store data. """
        self.source = jsontools.to_json(data)
    
    # Lookup rules
    lookups = {
        'title' : LR(
            'title',
            misc.obj_or_first
        ),
        'abstract' : LR('abstract'),
        'container-title' : LR('journal_title'),
        'container-title-short' : LR('journal_abbrev'),
        'volume' : LR('volume'),
        'issue' : LR('issue'),
        'issn' : LR('issn'),
        'PMID' : LR('pmid'),
        'DOI' : LR(
            'doi',
            misc.doi_clean
        ),
    }
    
    # Fetch class for lookups
    fetch = lookup.DictFetch
