"""
Gather parsers and validators from sources.
"""

# Import base class
from citparse import CitParse

# Import subclasses
from sources.highwire import citparse as _
from sources.wiley import citparse as _
from sources.plos import citparse as _
from sources.frontiers import citparse as _
from sources.nature import citparse as _
from sources.pubmed import citparse as _

# Import base class
from refparse import RefParse

# Import subclasses
from sources.highwire import refparse as _
from sources.wiley import refparse as _
from sources.plos import refparse as _
from sources.frontiers import refparse as _
from sources.nature import refparse as _
from sources.pubmed import refparse as _

# Import base class
from validate import Validate

# Import subclasses
from sources.highwire import validate as _
from sources.frontiers import validate as _
from sources.wiley import validate as _
from sources.plos import validate as _