"""
Reference parser for MIT Press journals.
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import csl
from ...util import name
from ...util import page
from ...util import regex
from ...util import lookup
from ...util import htmltools

LR = lookup.LookupRule

class MIT(refparse.RefParse):
    
    lookups = {
        'title' : LR('span.NLM_article-title'),
        'container-title' : LR(
            'span.citation_source-journal, span.citation_source-book'
        ),
        'issued' : LR(
            'span.NLM_year',
            lambda year: csl.clean_year(year)
        ),
        'publisher' : LR('span.NLM_publisher-name'),
        'publisher-place' : LR('span.NLM_publisher-loc'),
    }
    
    def _parse_author(self):
        """  """
        
        # Store text
        text = self.source.text()

        # Get year string
        if 'issued' in self.data:
            year = self.data['issued'][0]
        else:
            year_match = regex.year.search(text)
            if year_match:
                year = year_match.groups()[0]
            else:
                # Quit if year can't be inferred from text
                return
        
        # Wrap year in parentheses
        pyear = '\(\s*{0}\s*\)'.format(year)

        # Quit if year string not found
        if not re.search(pyear, text):#pyear not in text:
            return
    
        # Drop leading year string
        text = re.split(pyear, text)[0]#text.split(pyear)[0]
        
        # Clean text
        text = re.sub('\s*&\s*', ' ', text, flags=re.I)

        # Split author string by comma
        authors = text.split('., ')
        
        # Initialize CSL list
        authors_csl = []
        
        # Convert each author to CSL
        for author in authors:
            
            # Parse to CSL
            csl = name.human_to_csl(author)
            
            # Append to CSL list
            authors_csl.append(csl)
        
        # Return CSL list
        return authors_csl

    fpage_key = 'span.NLM_fpage'
    lpage_key = 'span.NLM_lpage'

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'a.ref[href]',
            regex.doi
        )
