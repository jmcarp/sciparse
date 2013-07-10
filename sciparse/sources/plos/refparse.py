"""
Reference parser for PLoS journals.
"""

# Imports
import re

# Project imports
from ... import refparse
from ...util import name
from ...util import regex
from ...util import lookup

# Alias LookupRule for convenience
LR = lookup.LookupRule

class PLoS(refparse.RefParse):
    """ Parse HTML-formatted references from PLoS. """
    
    def __init__(self, html):
        
        # Call parent constructor
        super(PLoS, self).__init__(html)
        
        # Save text
        self.text = self.source.text()

    # Lookups for extracting reference meta-data
    # from <meta> tags
    meta_lookups = {
        'title' : LR('title'),
        'pages' : LR('pages'),
        'volume' : LR('volume'),
        'issued' : LR(
            'date',
            lambda year: [int(year)]
        ),
    }
    
    def _parse00_meta_fields(self):
        """PLoS provides some reference meta-data in the 
        bioliography and more in <meta name="citation_reference" ...>
        tags. This function extracts available reference info from
        the <meta> tags. Fields in <meta>s are delimited by ';', and 
        keys and values are delimited by '=':

        <meta name="citation_reference" content="citation_title=An Indo-Pacific goby (Teleostei: Gobioidei) from West-Africa, with systematic notes on Butis and related eleotridine genera; citation_volume=23; citation_number=4; citation_pages=311-324; citation_date=1989; " />

        Returns:
            CSL-formatted reference info

        """
        # Extract content from <meta>
        meta_content = self.source('meta')\
            .attr('content')\
            .strip('; ')
        
        # Split into fields
        meta_parts = re.split(
            r';(?=\scitation_)', 
            meta_content, 
            flags=re.I
        )
        
        # Initialize data
        meta_data = {}

        # Iterate over parts
        for meta_part in meta_parts:

            # Split part by '='
            part_split = re.split(r'(?<=\w)=', meta_part, flags=re.I)

            # Skip if number of parts != 2
            if len(part_split) != 2:
                continue
            
            # Get key
            key = part_split[0]

            # Remove initial 'citation_'
            key = key.replace('citation_', '')
            
            # Remove remaining whitespace
            key = key.strip()

            # Get value
            val = part_split[1].strip()

            # Add value to data
            meta_data[key] = val
        
        # Return parsed data
        return lookup.DictFetch(meta_data)\
            .fetch(self.meta_lookups)
    
    def _parse_author(self):
        """  """
        
        # Strip leading digits
        text = self.text
        text = re.sub('^\d+\.\s+', '', text)
        
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
        pyear = '({0})'.format(year)
        
        # Quit if year string not found
        if pyear not in text:
            return
    
        # Drop leading year string
        text = text.split(pyear)[0]

        # Split author string by comma
        authors = text.split(', ')
        
        # Initialize CSL list
        authors_csl = []
        
        # Convert each author to CSL
        for author in authors:
            
            # Insert comma before initials
            author = re.sub(r'[A-Z]+\s*$', r',\g<0>', author)
            
            # Parse to CSL
            csl = name.human_to_csl(author)
            
            # Append to CSL list
            authors_csl.append(csl)
        
        # Return CSL list
        return authors_csl

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return self.source('ul[data-doi]').attr('data-doi')
