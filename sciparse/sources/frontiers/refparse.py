"""
Reference parser for Frontiers journals.
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import name
from ...util import regex
from ...util import lookup
from ...util import htmltools

# Alias LookupRule for convenience
LR = lookup.LookupRule

class Frontiers(refparse.RefParse):
    """ Parse HTML-formatted references from PLoS. """
    
    def __init__(self, html, **kwargs):
        
        # Call parent constructor
        super(type(self), self).__init__(html, **kwargs)
        
        # Save text
        self.text = self.source.text()

    def _parse00_container_title_short(self):
        
        italics = self.source('i')
        if italics:
            return PyQuery(italics[-1]).text()

    def _parse00_issued(self):
        
        year_match = regex.year.search(self.text)
        if year_match:
            try:
                year = int(year_match.groups()[0])
                return [year]
            except ValueError:
                return
    
    def _parse01_author(self):
        
        # Quit if date not available
        if 'issued' not in self.data:
            return

        year = self.data['issued'][0]
        pyear = '({0})'.format(year)

        if pyear not in self.text:
            return

        authors_raw = self.text\
            .split(pyear)[0]\
            .split('., ')
        
        authors_csl = []

        for author_raw in authors_raw:

            author_csl = name.human_to_csl(author_raw)
            authors_csl.append(author_csl)

        return authors_csl

    def _parse01_title(self):
        
        # Quit if date or journal not available
        if 'issued' not in self.data or \
                'container-title-short' not in self.data:
            return
        
        title_ptn = r'''
            \({0}\)\.       # Year wrapped in ()
            (.*?)           # Title group
            {1}             # Journal title
        '''.format(
            self.data['issued'][0],
            self.data['container-title-short'].replace(' ', '\ ')
        )
        
        title_match = re.search(title_ptn, self.text, re.X | re.M | re.S)

        if title_match:
            return title_match.groups()[0].strip()

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return htmltools.parse_link(
            self.source,
            'p.ReferencesCopy2 a[href]',
            regex.doi
        )
    
    pmid_pattern = re.compile(r'TermToSearch=(\d+)')
    def _parse_PMID(self):
        """ Extract PMID from reference. """
        
        return htmltools.parse_link(
            self.source,
            'p.ReferencesCopy2 a[href]',
            self.pmid_pattern
        )
