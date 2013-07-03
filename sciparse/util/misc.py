"""
"""

# Imports
import re
import os, errno

# Taken from http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


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

def doi_clean(doi):
    """Remove extraneous text from DOI string.

    :param doi: DOI string

    >>> doi_clean('http://dx.doi.org/10.1016/j.neuroimage.2012.07.004')
    '10.1016/j.neuroimage.2012.07.004'
    >>> doi_clean('dx.doi.org/10.1016/j.neuroimage.2012.07.004')
    '10.1016/j.neuroimage.2012.07.004'
    >>> doi_clean('doi:10.1016/j.neuroimage.2012.07.004')
    '10.1016/j.neuroimage.2012.07.004'

    """
    # Strip whitespace
    doi = doi.strip()

    # Strip leading URL
    doi = re.sub('(?:http://)?dx\.doi\.org/', '', doi, flags=re.I)

    # Strip leading 'doi:'
    doi = re.sub('doi:', '', doi, flags=re.I)

    return doi

def obj_or_first(thing):
    
    return get_singleton(thing, force=True)   

def get_singleton(thing, force=False, uniq=False):
    """Extract 0th item from list if singleton, else 
    return input.

    :param thing: Potential singleton list
    :param force: Force result to be singleton
    :param uniq: Reduce list to unique elements
    
    >>> get_singleton([1, 2, 3])
    [1, 2, 3]
    >>> get_singleton([1, 2, 3], force=True)
    1
    >>> get_singleton([2])
    2

    """
    
    # Return thing[0] if thing is one-element list
    if isinstance(thing, list):
        if force:
            return thing[0]
        if uniq:
            uthing = []
            for th in thing:
                if th not in uthing:
                    uthing.append(th)
            thing = uthing
        if len(thing) == 1:
            return thing[0]
    
    # Return original thing
    return thing

# Run doctests
if __name__ == '__main__':
    import doctest
    doctest.testmod()
