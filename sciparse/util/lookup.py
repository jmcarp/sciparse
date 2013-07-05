"""
"""

# Imports
import abc

class LookupRule(object):
    
    def __init__(self, field, fun=lambda i: i):
        
        # Memorize arguments
        self.field = field
        self.fun = fun

    def __repr__(self):
        
        return 'LookupRule({0})'.format(self.field)

class LookupFetch(object):
    
    # Abstract class
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def extract(self, lookup):
        pass
    
    def __init__(self, data):
        
        # Memorize data
        self.data = data

    def fetch(self, lookups):
        """
        """
        # Initialize result
        result = {}
        
        # Iterate over field rules
        for lookname in lookups:
            
            # Get lookup parts
            field = lookups[lookname].field
            fun = lookups[lookname].fun

            # Skip if field is falsy
            if not field:
                continue

            # Extract value from HTML
            value = self.extract(field)

            # Quit if value is falsy
            if not value:
                continue
            
            # Singleton list -> value
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
         
            # Add value if available
            if value:
                fvalue = fun(value)
                if fvalue:
                    result[lookname] = fvalue
        
        # Return completed fields
        return result

class HTMLFetch(LookupFetch):
    
    def extract(self, lookup):
        return self.data(lookup).text()

class DictFetch(LookupFetch):
    
    def extract(self, lookup):
        return self.data.get(lookup, None)
