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

class APA_PSYCNet(refparse.RefParse):
    
    lookups = {
        'container-title' : LR('cite.citationSource'),
    }

    def _parse_issued(self):
        
        year_match = regex.year.search(self.source.text())
        if year_match:
            year = year_match.groups()[0]
            return [year]

    def _parse_author(self):
        
        # Get name parts
        name_parts = self.source('''
            span.surname,
            span.givenNames,
            span.suffix
        ''')
        
        # Initialize author list
        authors = []
        
        # Initialize name
        author = HumanName()
        
        # Loop over name parts
        for name_part in name_parts:
            
            # PyQuer-ify part
            q_name_part = PyQuery(name_part)
            
            # Handle surname
            if q_name_part('.surname'):
                
                if author:
                    authors.append(name.human_to_csl(author))

                author = HumanName()
                author.last = q_name_part.text()
            
            # Handle given name
            elif q_name_part('.givenNames'):
                
                author.first = q_name_part.text()
            
            # Handle suffix
            elif q_name_part('.suffix'):
                
                author.suffix = q_name_part.text()
            
        # Append final name if truthy
        if author:

            authors.append(name.human_to_csl(author))

        # Return author list
        return authors

    def _parse_DOI(self):
        
        return htmltools.parse_link(
            self.source, 
            'ul.refListItemLinks a[href]',
            regex.doi
        )
