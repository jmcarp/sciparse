"""
"""

# Imports
import json

# Project imports
from .. import CitParse, RefParse

def citelet_to_citparse_fixture(payload, fixture_name):
    """

    :param payload:
    :param fixture_name:

    """
    # Load Citelet payload
    citelet_data = json.load(open(payload))
    publisher = citelet_data['publisher']

    # Parse Citelet payload
    parser = CitParse.get(publisher)(citelet_data['citation'])
    csl = parser.parse()

    # Save fixture
    make_fixture(
        publisher,
        citelet_data['citation'],
        csl,
        fixture_name
    )

def citelet_to_refparse_fixture(payload, ref_list, base_fixture_name):
    """

    :param payload:
    :param ref_list:
    :param base_fixture_name:

    """
    # Load Citelet payload
    citelet_data = json.load(open(payload))
    publisher = citelet_data['publisher']
    references = citelet_data['references']
    
    # Loop over target references
    for ref_idx in ref_list:

        # Quit if reference doesn't exist
        if ref_idx >= len(references):
            continue

        # Build fixture name
        fixture_name = '{0}_ref{1}.json'.format(base_fixture_name, ref_idx)

        # Parse Citelet payload
        parser = RefParse.get(publisher)(references[ref_idx])
        csl = parser.parse()
        
        # Save fixture
        make_fixture(
            publisher,
            citelet_data['references'][ref_idx],
            csl,
            fixture_name
        )

def make_fixture(pub, raw, csl, out):
    """Generate fixture containing raw reference HTML
    and the corresponding CSL-formatted object. Write to file.
    
    :param pub:
    :param raw:
    :param csl:
    :param out:
    
    """
    # 
    with open(out, 'w') as fp:
        json.dump({
            'pub' : pub,
            'raw' : raw,
            'csl' : csl,
        }, fp, indent=4)
