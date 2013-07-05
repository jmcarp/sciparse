"""
highwire source validator
verifies JSON
Author: Harry Rybacki
Date: 11June13
"""

# Project imports
from ... import validate

class PLOS(validate.Validate):

    citation_required = [
        'title',
        'journal_title',
        'author',
        'date',
    ]
