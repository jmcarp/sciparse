"""
"""

# Imports
import re
from pyquery import PyQuery
from nameparser import HumanName

# Project imports
from ... import refparse
from ...util import name
from ...util import regex
from ...util import lookup
from ...util import htmltools

# Alias LookupRule for convenience
LR = lookup.LookupRule

class APA_EBSCO(refparse.RefParse):
    
    def _parse_issued(self):
        
        year_match = regex.year.search(self.source.text())
        if year_match:
            year = year_match.groups()[0]
            return [year]

    def _parse_DOI(self):
        
        doi_match = regex.doi.search(self.source.text())
        if doi_match:
            return doi_match.groups()[0]
