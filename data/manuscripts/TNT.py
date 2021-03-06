#!/usr/bin/env python
# encoding: utf-8

msID = 10

import sys, os, re, unicodedata
from datetime import date
from django.core.management import setup_environ
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../')) #There's probably a better way of doing this
from openscriptures import settings
setup_environ(settings)
from openscriptures.data.unbound_bible import UNBOUND_CODE_TO_OSIS_CODE # Why does this have to be explicit?
from openscriptures.core.models import *


"""
What is included are the page-numbers of the print edition, the section and
paragraph breaks (in the printed edition the former are marked by a blank line,
the latter by simple indentation of the first line of the paragraph), the
punctuation of the text, and the accentuation as given by Tregelles. The title
and subscription at the end of each book are also included.
"""

""" http://www.tyndalehouse.com/tregelles/page2.html:
The Greek New Testament,
Edited from Ancient Authorities, with their
Various Readings in Full,
and the
Latin Version of Jerome,

by Samuel Prideaux Tregelles, LL.D.

London.
Samuel Bagster and Sons: Paternoster Row.
C. J. Stewart: King William Street, West Strand.
1857–1879.

Transcription of TNT and TNT2
edited by Dirk Jongkind,

in collaboration with Julie Woodson,
Natacha Pfister, and Robert Crellin.

Consultant editor: P.J. Williams

Tyndale House, Cambridge
2009.
"""

Work.objects.filter(id=10).update(unified_work=None).delete()
msWork = Work(
    id           = 10,
    title        = "Tragelles' Greek New Testament",
    abbreviation = 'Tragelles',
    language     = Language('grc'),
    type         = 'Bible',
    osis_slug    = 'TNT',
    publish_date = date(1879, 1, 1),
    originality  = 'manuscript-edition',
    creator      = "Samuel Prideaux Tregelles, LL.D.",
    url          = "http://www.tyndalehouse.com/Download/TNT%201.0.0.zip",
    license      = License.objects.get(url="http://creativecommons.org/licenses/by-nc-sa/3.0/")
)
msWork.save()
