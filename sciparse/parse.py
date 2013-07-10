"""
Defines abstract base class for sciparse parsers. Subclassed
by citparse.py and refparse.py.
"""

# Imports
import re
import inspect

# Project imports
from util import page
from util import xref

class Parse(object):
    """Base class for sciparse parsers. Subclasses may define
    lookups (dictionary mapping field names to lookup.LookupRule
    instances), method-based parsers (e.g. _parse_author, 
    _parse_title, etc.), and a fetch class (lookup.DictFetch
    or lookup.HTMLFetch).

    """
    # Get citation meta-data from CrossRef
    ping_doi = False

    def parse(self):
        """Run lookup- and method-based parsers, then optionally
        ping DOI for additional reference information.

        """       
        # Initialize data
        self.data = {}

        # Extract data from lookup fields
        self.parse_lookup_fields()
        
        # Extract data from custom methods
        self.parse_method_fields()
        
        # Add data from DOI if available
        if self.ping_doi and 'DOI' in data:
            doi_data = xref.doi_to_csl(data['DOI'])
            self.data.update(doi_data)

        # Return data
        return self.data
    
    def parse_method_fields(self):
        """Use parse methods to extract various fields
        from article data. Method-based parsers are any
        methods beginning with _parse\d*_. To control order
        of method-based parsers, use names like 
        _parse00_title and _parse01_author.

        """
        # Get field methods
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        methods = [m for m in methods if m[0].startswith('_parse')]
        methods = sorted(methods, key=lambda m: m[0])

        # Iterate over field methods
        for method in methods:

            # Call method
            value = method[1]()

            # Update data if result is dict
            if isinstance(value, dict):
                self.data.update(
                    {k:value[k] for k in value if value[k]}
                )
            # Else store value in data
            else:
                # Get method name
                field = method[0]
                field = re.sub('_parse\d*_', '', field)
                field = field.replace('_', '-')
                # Store value if truthy
                if value:
                    self.data[field] = value

    def parse_lookup_fields(self):
        """Parse simple lookup fields. Defined in self.lookups.

        """
        # Quit if no lookups or no fetch
        if not hasattr(self, 'lookups') or \
                not hasattr(self, 'fetch') or \
                not hasattr(self, 'source'):
            return {}
        
        # Fetch info from source
        info = self.fetch(self.source)\
            .fetch(self.lookups)
        
        # Add info to data
        self.data.update(info)
    
    # Generic page extraction
    fpage_key = None
    lpage_key = None
    def _parse_pages(self):
        """ Extract page range. """
        
        return page.fetch_pages(
            self, 
            self.fpage_key,
            self.lpage_key
        )
