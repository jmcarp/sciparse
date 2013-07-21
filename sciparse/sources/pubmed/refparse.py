"""
"""

# Imports
import re

# Project imports
from ... import refparse
from ...util import csl
from ...util import regex
from ...util import lookup
from ...util import htmltools

# Alias LookupRule
LR = lookup.LookupRule

class Pubmed(refparse.RefParse):
    
    lookups = {
        'title' : LR('span.ref-title'),
        'container-title-short' : LR('span.ref-journal'),
        'issued' : LR(
            'span.year',
            lambda year: csl.clean_year(year)
        ),
        'volume' : LR('span.ref-vol'),
    }
    
    def _parse_DOI(self):
        
        doi_match = regex.doi.search(self.html)
        if doi_match:
            return doi_match.groups()[0]

    pmid_pattern = re.compile(r'''
        (?:                         # Begin pre-PMID group
            pubmed/                 # One pre-PMID pattern
            |                       # OR
            pubmed&article-id=      # Another pre-PMID pattern
        )                           # End pre-PMID group
        (\d+)                       # Capture PMID
        ''', re.I | re.X)
    def _parse_PMID(self):
        
        return htmltools.parse_link(
            self.source, 
            'span.pubmed a[href]',
            self.pmid_pattern
        )

    pmcid_pattern = re.compile(r'pmc/articles/pmc(\d+)', re.I)
    def _parse_PMCID(self):
        
        return htmltools.parse_link(
            self.source, 
            'span.pmc a[href]',
            self.pmcid_pattern
        )
