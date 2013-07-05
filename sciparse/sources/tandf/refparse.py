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

class TandF(refparse.RefParse):
    
    lookups = {
        'issued' : LR(
            'span.NLM_year',
            csl.clean_year
        ),
        'volume' : LR('span.ref-vol'),
    }
    
    def _parse_author(self):
        
        return self.source('a[href^="/action/doSearch?"]').map(
            lambda: name.human_to_csl(this.text)
        )

    def _parse00_container_title(self):
        
        italics = self.source('i')
        if italics:
            return PyQuery(italics[-1]).text()

    def _parse_DOI(self):
        
        doi_match = regex.doi.search(self.html)
        if doi_match:
            return doi_match.groups()[0]
