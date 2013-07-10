# -*- coding: utf-8 -*- #

"""
"""

# Imports
import re

# Project imports
from ... import refparse
from ...util import name
from ...util import page
from ...util import regex
from ...util import lookup
from ...util import htmltools

# Alias LookupRule for convenience
LR = lookup.LookupRule

class ScienceDirect(refparse.RefParse):
    
    lookups = {
        'title' : LR('li.title'),
        'author' : LR(
            'li.author',
            lambda author: map(name.human_to_csl, author.split(','))
        ),
    }

    def _parse_issued(self):
        """ Extract pages from reference. """
        
        year_match = regex.year.search(self.source.text())
        if year_match:
            year = year_match.groups()[0]
            return [year]
    
    source_rgx = re.compile(ur'''
        (?P<journal>[\w\s\.]+)    # Journal title
        ,\s                       # Spacing
        (?P<volume>\d+)           # Volume
        \s                        # Spacing
        \((?P<year>\d{4})\)       # Year
        ,\s                       # Spacing
        pp\.                      # Page indicator
        \s                        # Spacing
        (?P<fpage>\d+)            # First page
        (?:                       # Begin optional
            –                     # Page separator
            (?P<lpage>\d+)        # Last page
        )?                        # End optional
    ''', re.I | re.X)
    def _parse_source(self):
        """ScienceDirect defines a "source" field containing
        journal title, volume, year, and pages. This method attempts
        to parse the source text using a regular expression.

        """
        # Get source text
        source_text = self.source('li.source').text()
        
        # Quit if no source text
        if not source_text:
            return
        
        # Test against source pattern
        source_match = self.source_rgx.search(source_text)
        
        # Quit if no match
        if not source_match:
            return
        
        # Extract named fields from match
        source_result = source_match.groupdict()
        
        # Initialize CSL result
        result = {}
        
        # Add fields to CSL
        result['container-title-short'] = source_result['journal']
        result['volume'] = source_result['volume']
        
        # Add page to CSL
        page_info = page.page_to_csl(
            result.get('fpage', None),
            result.get('lpage', None)
        )
        if page_info:
            result.update(page_info)

        # Return CSL result
        return result

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        doi_match = regex.doi.search(self.source.text())
        if doi_match:
            return doi_match.groups()[0]
