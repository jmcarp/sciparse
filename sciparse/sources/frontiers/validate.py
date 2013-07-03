"""
highwire source validator
verifies JSON
Author: Harry Rybacki
Date: 11June13
"""

# Project imports
from ... import validate

class Frontiers(validate.Validate):

    required_head = [
        'title',
        'journal_title',
        'author',
        'publication_date',
    ]
