"""
"""

# Project imports
from util import magic
from util import jsontools

def check_fields(dict, fields):
    """ Check that fields are in dictionary; raise AttributeError
    if any fields missing.

    :param dict: Dictionary to check
    :param fields: Fields that should be in dict

    """
    # Loop over fields
    for field in fields:
        if field not in dict or \
                not dict[field]:
            raise AttributeError('Missing field: {0}'.format(field))

@magic.regify
class Validate(object):
    
    # Required fields
    required = [
        'url',
        'publisher',
        'citation',
        'references',
        'meta',
    ]

    def __init__(self, data):
        """ Initialize and store data to be validated.

        :param data: JSON-formatted object or string

        """
        # Ensure that input is JSON
        self.data = jsontools.to_json(data)

    def validate(self):
        """ Validate data. """
        
        # Check for required fields
        check_fields(self.data, self.required)

        # Check for required fields
        if hasattr(self, 'citation_required'):
            check_fields(self.data['citation'], self.citation_required)
