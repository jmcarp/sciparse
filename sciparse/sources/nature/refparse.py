"""
Reference parser for Nature journals.
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import name
from ...util import page
from ...util import regex
from ...util import lookup
from ...util import htmltools

# Alias LookupRule
LR = lookup.LookupRule

class Nature(refparse.RefParse):
    """Nature uses two references formats. One, used by the flagship journals
    (Nature, Nature Neuroscience, etc.), wraps references in <div id="ref1"> tags.
    The other, used in other journals (e.g., Neuropsychopharmacology), wraps
    references in <div id="bib1"> tags. The __new__ method of Nature detects which
    format was used and returns an instance of the appropriate subclass.

    """
    def __new__(cls, html, qhtml=None, dispatch=True):
        """

        :param html:
        :param dispatch:

        """
        
        # Call superclass __new__ if dispatch is off
        if not dispatch:
            return super(Nature, cls).__new__(cls, html)
        
        # Parse HTML
        html, qhtml = htmltools.parse_html(html)
        
        # Dispatch to correct subclass
        # On dispatch, must set dispatch to False so that subclass
        # __new__ methods don't try to dispatch again
        if qhtml('li[id^="ref"]'):
            return _NatureV1(html, qhtml, dispatch=False)
        if qhtml('li[id^="bib"]'):
            return _NatureV2(html, qhtml, dispatch=False)
    
    def __init__(self, html, qhtml=None, **kwargs):
        """Initialize Nature instance. Signature must include **kwargs to allow
        for optional parameters needed by Nature.__new__, i.e. dispatch.
        
        :param html: HTML to parse

        """
        # Call parent constructor
        super(Nature, self).__init__(html, **kwargs)
        
        # Save text
        self.text = self.source.text()

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'a[href]',
            regex.doi
        )
    
    pmid_pattern = re.compile(r'list_uids=(\d+)', re.I)
    def _parse_PMID(self):
        """ Extract PMID from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'a[href]',
            self.pmid_pattern
        )

    isi_pattern = re.compile(r'keyUT=(\d+)', re.I)
    def _parse_ISI(self):
        """ Extract ISI ID from reference. """
        
        return htmltools.parse_link(
            self.source, 
            'a[href]',
            self.isi_pattern
        )

class _NatureV1(Nature):
    
    lookups = {
        'title' : LR('span.title'),
        'container-title-short' : LR('span.source-title'),
        'issued' : LR(
            'span.year',
            lambda year: [int(year)]
        ),
        'volume' : LR('span.vol'),
    }
    
    def _parse_author(self):
        """ Extract CSL-formatted authors. """
        
        # Initialize CSL authors
        csl_authors = []
        
        # Get author HTML snippets
        html_authors = self.source('span.author').map(
            lambda: PyQuery(this).text()
        )
        
        # Parse authors to CSL
        for author in html_authors:

            csl_author = name.human_to_csl(author)
            if csl_author:
                csl_authors.append(csl_author)

        # Return CSL authors
        return csl_authors
    
    def _parse_pages(self):
        """ Extract CSL-formatted page range. """
            
        # Extract page range
        frst = self.source('span.start-page').text()
        last = self.source('span.end-page').text()
        
        # Parse page range to CSL
        return page.page_to_csl(frst, last)

class _NatureV2(Nature):
    
    lookups = {
        'container-title-short' : LR('span.journal'),
        'issue' : LR('span.jnumber'),
    }

    def _parse00_issued(self):
        
        year_match = regex.year.search(self.text)
        if year_match:
            try:
                year = int(year_match.groups()[0])
                return [year]
            except ValueError:
                return
    
    def _parse01_author(self):
        
        # Quit if date not available
        if 'issued' not in self.data:
            return
        
        # Get ()-wrapped year
        year = self.data['issued'][0]
        pyear = '({0})'.format(year)
        
        # Quit if year string not found
        if pyear not in self.text:
            return

        authors_raw = self.text\
            .split(pyear)[0]\
            .split('., ')
        
        # Initialize CSL-formatted authors
        authors_csl = []

        for author_raw in authors_raw:

            author_csl = name.human_to_csl(author_raw)
            if author_csl:
                authors_csl.append(author_csl)
        
        # Return CSL-formatted authors
        return authors_csl
