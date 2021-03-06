#!/usr/bin/env python
# encoding: utf-8

msID = 4

import sys, os, re, unicodedata, urllib, zipfile, StringIO
from datetime import date
from django.core.management import setup_environ
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../')) #There's probably a better way of doing this
from openscriptures import settings
setup_environ(settings)
from openscriptures.core.models import *
from openscriptures.data import import_helpers

# Abort if MS has already been added (or --force not supplied)
import_helpers.abort_if_imported(msID)

# Download the source file
source_url = "http://files.morphgnt.org/tischendorf/Tischendorf-2.5.zip"
import_helpers.download_resource(source_url)

import_helpers.delete_work(msID)
msWork = Work(
    id           = msID,
    title        = "Tischendorf 8th ed. v2.5 (Qere)",
    language     = Language('grc'),
    type         = 'Bible',
    osis_slug    = 'Tischendorf',
    publish_date = date(2009, 1, 1),
    originality  = 'manuscript-edition',
    creator      = "<a href='http://en.wikipedia.org/wiki/Constantin_von_Tischendorf' title='Constantin von Tischendorf @ Wikipedia'>Constantin von Tischendorf</a>. Based on G. Clint Yale's Tischendorf text and on Dr. Maurice A. Robinson's Public Domain Westcott-Hort text. Edited by <a href='http://www.hum.aau.dk/~ulrikp/'>Ulrik Sandborg-Petersen</a>.",
    url          = source_url,
    license      = License.objects.get(url="http://creativecommons.org/licenses/publicdomain/")
)
msWork.save()


bookFilenameLookup = {
	'Matt'   : "MT.txt"   ,
	'Mark'   : "MR.txt"   ,
	'Luke'   : "LU.txt"   ,
	'John'   : "JOH.txt"  ,
	'Acts'   : "AC.txt"   ,
	'Rom'    : "RO.txt"   ,
	'1Cor'   : "1CO.txt"  ,
	'2Cor'   : "2CO.txt"  ,
	'Gal'    : "GA.txt"   ,
	'Eph'    : "EPH.txt"  ,
	'Phil'   : "PHP.txt"  ,
	'Col'    : "COL.txt"  ,
	'1Thess' : "1TH.txt"  ,
	'2Thess' : "2TH.txt"  ,
	'1Tim'   : "1TI.txt"  ,
	'2Tim'   : "2TI.txt"  ,
	'Titus'  : "TIT.txt"  ,
	'Phlm'   : "PHM.txt"  ,
	'Heb'    : "HEB.txt"  ,
	'Jas'    : "JAS.txt"  ,
	'1Pet'   : "1PE.txt"  ,
	'2Pet'   : "2PE.txt"  ,
	'1John'  : "1JO.txt"  ,
	'2John'  : "2JO.txt"  ,
	'3John'  : "3JO.txt"  ,
	'Jude'   : "JUDE.txt" ,
	'Rev'    : "RE.txt"   ,   
}

# - One word per line
# - Space-separated fields (except for the last two)
# - - fields:
#   0. Book (corresponds to the filename, which is the Online Bible standard)
#   1. Chapter:Verse.word-within-verse
#   2. Pagraph break ("P") / Chapter break ("C") / No break (".") (see
#      below)
#   3. The text as it is written in the printed Tischendorf (Kethiv)
#   4. The text as the editor thinks it should have been (Qere)
#   5. The morphological tag (following the Qere)
#   6. The Strong's number (following the Qere)
#   7. The lemma in two versions:
#     7.a The first version, which corresponds to The NEW Strong's
#       Complete Dictionary of Bible Words.
#     7.b Followed by the string " ! "
#     7.c Then the second version, which corresponds to Friberg, Friberg
#       and Miller's ANLEX.
#     There may be several words in each lemma.
# 
# All Strong's numbers are single numbers with 1,2,3, or 4 digits.

#puncchrs = re.escape(''.join(unichr(x) for x in range(65536) if unicodedata.category(unichr(x)) == 'Po'))
puncchrs = re.escape(ur'.·,;:!?"\'')
lineParser = re.compile(ur"""^
        (?P<book>\S+)\s+            # Book (corresponds to the filename, which is the Online Bible standard)
        (?P<chapter>\d+):           # Chapter
        (?P<verse>\d+)\.            # Verse
        (?P<position>\d+)\s+        # word-within-verse
        (?P<break>\S)\s+            # Pagraph break ("P") / Chapter break ("C") / No break (".") 
        (?P<kethiv>\S+?)            # The text as it is written in the printed Tischendorf (Kethiv)
        (?P<kethivPunc>[%s])?\s+    # Kethiv punctuation
    (?P<rawParsing>
        (?P<qere>\S+?)              # The text as the editor thinks it should have been (Qere)
        (?P<qerePunc>  [%s])?\s+    # Qere punctuation
        (?P<morph>\S+)\s+           # The morphological tag (following the Qere)
        (?P<strongsNumber>\d+)\s+   # The Strong's number (following the Qere)
        (?P<strongsLemma>.+?)       # Lemma which corresponds to The NEW Strong's Complete Dictionary of Bible Words. (There may be several words in each lemma.)
        \s+!\s+                     # A " ! " separates the lemmas
        (?P<anlexLemma>.+?)         # Lemma which corresponds to Friberg, Friberg and Miller's ANLEX. (There may be several words in each lemma.)
    )
    \s*$""" % (puncchrs, puncchrs),
    re.VERBOSE
)

bookRefs = []
bookTokens = []
precedingTokenCount = 0

zip = zipfile.ZipFile(os.path.basename(source_url))
for book_code in OSIS_BIBLE_BOOK_CODES:
    print OSIS_BOOK_NAMES[book_code]
    
    precedingTokenCount = precedingTokenCount + len(bookTokens)
    bookTokens = []
    chapterRefs = []
    verseRefs = []
    
    # Set up the book ref
    bookRef = Ref(
        work = msWork,
        type = Ref.BOOK,
        osis_id = book_code,
        position = len(bookRefs),
        title = OSIS_BOOK_NAMES[book_code]
    )
    
    for line in StringIO.StringIO(zip.read("Tischendorf-2.5/Unicode/" + bookFilenameLookup[book_code])):
        line = unicodedata.normalize("NFC", unicode(line, 'utf-8'))
        
        word = lineParser.match(line)
        if word is None:
            print " -- Warning: Unable to parse line: " + line 
            continue
        
        # If this is a paragraph break, insert new paragraph token
        if(word.group('break') == 'P'):
            token = Token(
                data     = "¶",
                type     = Token.PUNCTUATION,
                work     = msWork,
                position = precedingTokenCount + len(bookTokens)
            )
            token.save()
            bookTokens.append(token)
        
        # Insert token
        token = Token(
            data     = word.group('qere'),
            type     = Token.WORD,
            work     = msWork,
            position = precedingTokenCount + len(bookTokens)
        )
        token.save()
        bookTokens.append(token)
        
        # Token Parsing
        parsing = TokenParsing(
            token = token,
            parse = word.group('morph'),
            strongs = word.group('strongsNumber'),
            lemma = word.group('strongsLemma') + '; ' + word.group('anlexLemma'),
            language = Language('grc'),
            work = msWork
        )
        parsing.save()
        
        # Insert punctuation
        if(word.group('qerePunc')):
            token = Token(
                data     = word.group('qerePunc'),
                type     = Token.PUNCTUATION,
                work     = msWork,
                position = precedingTokenCount + len(bookTokens)
            )
            token.save()
            bookTokens.append(token)
        
        # Make this token the first in the book ref, and set the first token in the book
        if len(bookTokens) == 1:
            bookRef.start_token = bookTokens[0]
            bookRef.save()
            bookRefs.append(bookRef)
        
        # Set up the Chapter ref
        if(not len(chapterRefs) or word.group('chapter') != chapterRefs[-1].numerical_start):
            if(len(chapterRefs)):
                chapterRefs[-1].end_token = bookTokens[-2]
            chapterRef = Ref(
                work = msWork,
                type = Ref.CHAPTER,
                osis_id = ("%s.%s" % (book_code, word.group('chapter'))),
                position = len(chapterRefs),
                parent = bookRef,
                numerical_start = word.group('chapter'),
                start_token = bookTokens[-1]
            )
            chapterRef.save()
            chapterRefs.append(chapterRef)
        
        # Set up the Verse Ref
        if(not len(verseRefs) or word.group('verse') != verseRefs[-1].numerical_start):
            if(len(verseRefs)):
                verseRefs[-1].end_token = bookTokens[-2]
            verseRef = Ref(
                work = msWork,
                type = Ref.VERSE,
                osis_id = ("%s.%s" % (chapterRef.osis_id, word.group('verse'))),
                position = len(verseRefs),
                parent = chapterRefs[-1],
                numerical_start = word.group('verse'),
                start_token = token
            )
            verseRef.save()
            verseRefs.append(verseRef)
    
    #Save all books, chapterRefs, and verseRefs
    bookRef.end_token = bookTokens[-1]
    bookRef.save()
    chapterRefs[-1].end_token = bookTokens[-1]
    for chapterRef in chapterRefs:
        chapterRef.save()
    verseRefs[-1].end_token = bookTokens[-1]
    for verseRef in verseRefs:
        verseRef.save()
    
    
