"""
Reference parser for Springer journals.
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import regex
from ...util import htmltools

class Springer(refparse.RefParse):
    
    journal_rgx = re.compile('''
        (?P<journal>.*?)
        ,\s
        (?P<volume>\d+),$
    ''', re.I | re.X)
    def _parse_journal(self):
        
        journal_str = self.source('.EmphasisTypeItalic').text()
        if not journal_str:
            return

        journal_match = re.search(self.journal_rgx, journal_str)
        if not journal_match:
            return

        journal_data = journal_match.groupdict()

        result = {
            'container-title' : journal_data['journal'],
            'volume' : journal_data['volume'],
        }

        return result

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'span.OccurrenceDOI a[href]',
            regex.doi
        )

    pmid_pattern = re.compile(r'list_uids=(\d+)', re.I)
    def _parse_PMID(self):
        """ Extract PMID from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'span.OccurrencePID a[href]',
            self.pmid_pattern
        )
