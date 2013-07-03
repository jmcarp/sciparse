"""
"""

# Crash if file is executed directly
# See PEP 366
#if __package__ is None:
#    raise Exception('Can\'t execute directly. Use nosetests or python -m instead.')

# Imports
import json
import unittest

# Project imports
from .. import CitParse, RefParse

# Map fixture directories to parse classes
fixture_map = {
    'citparse' : CitParse,
    'refparse' : RefParse,
}

def add_tst_klass(name, fixture_type, fixture):
    """Create test class and add to global namespace.

    :param name: Name of the test
    :param fixture_type: Name of the fixture type [CitParse | RefParse]
    :param fixture: Path to the fixture JSON file

    """
    # Get fixture class
    fixture_klass = fixture_map[fixture_type]

    # Load fixture data
    fixture_data = json.load(open(fixture))
    
    # Initialize test class
    klass_name = '{0}_{1}_tests'.format(name, fixture_type)
    klass = type(klass_name, (unittest.TestCase,), {})

    # Initialize parser and attach to test class
    klass.parser = fixture_klass\
        .get(fixture_data['pub'])\
        (fixture_data['raw'])
    
    # Create test functions and add to test class
    for field in fixture_data['csl']:
        
        test = make_tst(field, fixture_data)
        
        # Add function to class
        method_name = 'test_{0}'.format(field)
        test.__name__ = method_name
        setattr(klass, method_name, test)
    
    # Add klass to global namespace
    globals()[klass_name] = klass

def make_tst(field, fixture_data):
    """  """
    
    def test(self):
        
        csl = self.parser.parse()
        self.assertEqual(
            fixture_data['csl'][field],
            csl[field]
        )

    return test

# Gather fixture JSON files and generate tests
import os
import glob
here = os.path.split(__file__)[0]

def add_tst_group(fixture_type):
    """
    """
    fixture_path = os.path.join(here, 'fixtures', fixture_type)
    fixtures = glob.glob(os.path.join(fixture_path, '*.json'))
    for fixture in fixtures:
        fixture_file = os.path.split(fixture)[1]
        fixture_name = os.path.splitext(fixture_file)[0]
        add_tst_klass(fixture_name, fixture_type, fixture)

# 
add_tst_group('citparse')
add_tst_group('refparse')

# Run tests
if __name__ == '__main__':
    unittest.main()
