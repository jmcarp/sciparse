"""
"""

import lookup
LR = lookup.LookupRule

def fetch_pages(parser, frst, last=None):
    """Extract page range from parser given page selectors.

    :param parser: Instance of sciparse.Parse
    :param frst: Fetch selector for first page
    :param last: Fetch selector for last page

    """
    # Fetch page values
    pages = parser\
        .fetch(parser.source)\
        .fetch({
            'frst' : LR(frst),
            'last' : LR(last),
        })
    
    # Convert to CSL format
    return page_to_csl(**pages)

def page_to_csl(frst, last=None):
    """Consume first and optional last page and produce
    CSL-formatted page range.

    :param frst: First page
    :param last: Last page

    Examples
    >>> page_to_csl('100', '110')
    {'pages': '100-110'}
    >>> page_to_csl('100')
    {'page': '100'}
    >>> page_to_csl('')

    """
    # Quit if no first page
    if not frst:
        return
    
    # Return first if not last
    # Return as a dictionary so that field is named
    # 'page', not 'pages'
    if not last:
        return {'page' : frst}
    
    # Return combined page string
    return {
        'pages' : '{0}-{1}'.format(frst, last)
    }

# Run doctests
if __name__ == '__main__':
    import doctest
    doctest.testmod()
