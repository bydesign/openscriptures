import re, os, sys

importScripts = (
    'greek_WH_UBS4_parsed.py',
    'Tischendorf-2.5.py',
    'greek_byzantine_2000_parsed.py',
    'greek_byzantine_2005_parsed.py',
    'greek_textus_receptus_parsed.py',
    #'TNT.py',
    #'TNT2.py', #We should be able to pass a command line argument to indicate which (TNT or TNT2) are desired
)
for script in importScripts:
    print "## %s ##" % script
    #execfile(script)
    os.system('python ' + script + ' ' + ''.join(sys.argv[1:]))
