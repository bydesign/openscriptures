#!/usr/bin/env python
# encoding: utf-8

import re, unicodedata, os, urllib, sys
from openscriptures.core.models import *

def normalize_token(data):
    # credit: http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
    data = unicodedata.normalize('NFC', ''.join((c for c in unicodedata.normalize('NFD', data) if unicodedata.category(c) != 'Mn')).lower())
    data = re.sub(ur"['’]", '', data)
    return data


def download_resource(source_url):
    if(not os.path.exists(os.path.basename(source_url))):
        if(not os.path.exists(os.path.basename(source_url))):
            print "Downloading " + source_url
            urllib.urlretrieve(source_url, os.path.basename(source_url))


def abort_if_imported(msID):
    if(len(Work.objects.filter(id=msID)) and not (len(sys.argv)>1 and sys.argv[1] == '--force')):
        print " (already imported; pass --force option to delete existing work and reimport)"
        exit()

def delete_work(msID, *varMsIDs):
    for varMsID in varMsIDs:
        Work.objects.filter(id=varMsID).update(unified=None, base=None)
        Work.objects.filter(id=varMsID).delete()
    
    Token.objects.filter(work=msID).update(unified_token=None)
    Work.objects.filter(id=msID).update(unified=None)
    Work.objects.filter(id=msID).delete()