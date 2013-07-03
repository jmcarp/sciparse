"""
"""

# Imports
from dateutil.parser import parse as dateparse
import datetime

def date_to_csl(date):
    """Convert a date (either a string or datetime.date object)
    into CSL-formatted JSON.

    Args:
        date : String or datetime.date
    Returns:
        CSL-formatted representation of date

    Examples:
    >>> csl = date_to_csl('10/1/1985')
    >>> csl == {'date-parts' : [1985, 10, 1]}
    True
    >>> csl = date_to_csl(datetime.date(1991, 10, 13))
    >>> csl == {'date-parts' : [1991, 10, 13]}
    True
    """

    return {
        'date-parts' : date_to_parts(date),
    }

def date_to_parts(date):
    """
    """
    # Process multiple dates if list
    if isinstance(date, list):
        dates = map(date_to_parts, date)
        unique_dates = []
        for date in dates:
            if date not in unique_dates:
                unique_dates.append(date)
        if len(unique_dates) == 1:
            return unique_dates[0]
        return unique_dates
    
    # Parse date string if not date
    if not isinstance(date, datetime.date):

        # Parse date string
        try:
            date = dateparse(date)
        except ValueError:
            return

    # Extract date parts
    date_parts = [
        date.year,
        date.month,
        date.day,
    ]

    # Return date parts
    return date_parts

# Run doctests
if __name__ == '__main__':
    import doctest
    doctest.testmod()
