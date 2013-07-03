"""
"""

# Imports
import os
import json

from bs4 import BeautifulSoup as BS

def translate(string, translator):
    
    return reduce(
        lambda s, key: s.replace(key, translator[key]),
        translator,
        string
    )

doi_translator = {
    '.' : '_dot_',
    '/' : '_slash_',
}
def escape_doi(doi):
    
    return translate(doi, doi_translator)

#TODO: write this
def load_fixture():
    
    pass

class Fixture(object):
    
    # Fields to store in fixture
    fields = ['html', 'publisher', 'journal', 'doi', 'pmid']

    def __init__(
            self,
            html,
            publisher,
            journal,
            doi=None,
            pmid=None):
        
        # Get fixture data
        _locals = locals()
        self.fixture = {key : _locals[key] for key in fields}

    def save(self, fname, path):
        
        # Get file name
        if fname is None:
            if pmid:
                fname = pmid
            elif doi:
                fname = escape_doi(doi)
            else:
                raise Exception('No name or ID provided')
        
        # Save JSON to file
        fpath = os.path.join(path, fname) + '.json'
        with open(fpath, 'w') as fp:
            json.dump(self.fixture, fp, indent=4)

def mkfix(
        html,
        publisher,
        journal,
        pmid=None,
        doi=None,
        fname=None,
        path='fixtures'):
    """Create citation fixture in JSON.

    Args:
        html : Raw HTML for citation
    """
    # Drop linebreaks
    html = html.replace('\n', '')

    # Get fixture data
    fix = locals()
    
