"""
Reference parser for Hindawi journals.
"""

# Imports
import re

# Project imports
from ... import refparse
from ...util import regex
from ...util import lookup
from ...util import htmltools

LR = lookup.LookupRule

class Hindawi(refparse.RefParse):
    
    lookups = {
        'container-title' : LR('i'),
    }

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'span.reflinks a[href]',
            regex.doi
        )
    
    mathscinet_pattern = re.compile(r'mathscinet-getitem\?mr=(\w+)', re.I)
    def _parse_MathSciNet(self):
        
        return htmltools.parse_link(
            self.source,
            'span.reflinks a[href]',
            self.mathscinet_pattern
        )
