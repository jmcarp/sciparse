"""
Reference parser for Wiley journals.
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import name
from ...util import page
from ...util import regex
from ...util import lookup
from ...util import htmltools

LR = lookup.LookupRule

class Wiley(refparse.RefParse):
    
    lookups = {
        'title' : LR('span.articleTitle'),
        'container-title-short' : LR('span.journalTitle'),
        'issued' : LR(
            'span.pubYear',
            lambda year: [int(year)]
        ),
        'volume' : LR('span.vol'),
    }
    
    def _parse_author(self):
        
        # Initialize formatted authors
        csl_authors = []

        # Get author HTML snippets
        authors = self.source('span.author')
        
        # Loop over authors
        for author in authors:
            
            # Get author text
            text = PyQuery(author).text()

            # Insert comma before initials
            # Else nameparser.HumanName will fail
            text = re.sub(r'[A-Z]+\s*$', r',\g<0>', text)
            
            # Convert to CSL format
            csl_author = name.human_to_csl(text)
            
            # Append to author list
            csl_authors.append(csl_author)
        
        # Return formatted author
        return csl_authors
    
    fpage_key = 'span.pageFirst'
    lpage_key = 'span.pageLast'

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'ul.externalReferences a[href]',
            regex.doi
        )
    
    pmid_pattern = re.compile(r'/pmed\?id=(\d+)', re.I)
    def _parse_PMID(self):
        """ Extract PMID from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'ul.externalReferences a[href]',
            self.pmid_pattern
        )

    isi_pattern = re.compile(r'/isi\?id=(\d+)', re.I)
    def _parse_ISI(self):
        """ Extract ISI ID from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'ul.externalReferences a[href]',
            self.isi_pattern
        )
