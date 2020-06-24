# -*- coding: cp1252 -*-

#   test_openproject.py
#
#   Tests and demonstrates access to a FieldWorks project.
#
#   Platforms: Python .NET and IronPython
#
#   Copyright Craig Farrow, 2008 - 2018
#

from flexlibs import FLExInit
from flexlibs.FLExProject import FLExProject, FDA_ProjectError

# If your data doesn't match your system encoding (in the console) then
# redirect the output to a file: this will make it utf-8.
## BUT This doesn't work in IronPython!! Dec2018: not working when redirecting to a file. What has changed? TODO
import codecs
import sys
if sys.stdout.encoding == None:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)


#============ Configurables ===============

# Database to use
projectName = "Sena 3 Experiments"

      

def reportBasicInfo(project):
    # Global things in the Language Project

    #============ General Settings =======
    print "Last modified:", project.GetDateLastModified()
    print

    posList = project.GetPartsOfSpeech()
    print len(posList), "Parts of Speech:"
    for i in posList:
        print "\t", i
    print


    #============ Writing Systems ============

    # The names of WS associated with this DB. Sorted and with no duplicates.

    wsList = project.GetWritingSystems()
    print len(wsList), "Writing Systems in this database: (Language Tag, Handle)"
    print
    for x in wsList:
        name, langTag, handle, isVern = x
        print "\t", name
        print "\t\t", langTag, handle
        print "\t\t", "(Vernacular)" if isVern else "(Analysis)"
    print

    # A tuple of (language-tag, display-name)
    print "\tDefault vernacular WS = %s; %s" % project.GetDefaultVernacularWS()
    print "\tDefault analysis WS   = %s; %s" % project.GetDefaultAnalysisWS()
    print

    #============= Lexicon ================
    print "Custom Fields:"
    print "\tEntry level:"
    for cf in project.LexiconGetEntryCustomFields():
        # Tuple of flid and user-defined name:
        print "\t\t%s (%s)" % (cf[1], cf[0])
    print

    print "\tSense level:"
    for cf in project.LexiconGetSenseCustomFields():
        print "\t\t%s (%s)" % (cf[1], cf[0])
    print

    print "Lexicon contains %d entries" % project.LexiconNumberOfEntries()
    
    print "Text corpus contains %d texts" % project.TextsNumberOfTexts()

# -------------------------------------------------------------------    
if __name__ == "__main__":

    FLExInit.Initialize()
    
    project = FLExProject()

    try:
        project.OpenProject(projectName = projectName,
                            writeEnabled = False,
                            verbose = True)
    except FDA_ProjectError, e:
        print "OpenProject failed!"
        print e.message
        FLExInit.Cleanup()
        sys.exit(1)
        
    reportBasicInfo(project)
    
    FLExInit.Cleanup()
    
    