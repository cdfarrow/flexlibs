# -*- coding: cp1252 -*-

#   test_lexicon.py
#
#   Tests and demonstrates working with the FieldWorks lexicon.
#
#   Platforms: Python .NET and IronPython
#
#   Copyright Craig Farrow, 2008 - 2018
#

from flexlibs import FLExInit
from flexlibs.FLExProject import FLExProject, FDA_ProjectError

# If the data encoding doesn't match the system encoding (in the console) 
# then there may be garbage output. To see it properly redirect the 
# output to a file (the following code will make it utf-8.)
## BUT This doesn't work in IronPython!! Dec2018: not working when redirecting to a file. What has changed? TODO
import codecs
import sys
if sys.stdout.encoding == None:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout)


#============ Configurables ===============

# Database to use
projectName = "Demo - Sena 3"

# Maximum number of entries to print out; use
# a very big number for the whole lexicon.
LexiconMaxEntries = 5

# Enable writing tests
WriteTests = False


      
#--------------------------------------------------------------------
##
#ftflagsFlid = project.LexiconGetSenseCustomFieldNamed("FTFlags")
##print ftflagsFlid

#--------------------------------------------------------------------
def reportLexicalEntries(project):

    print "Listing up to %d lexical entries:" % LexiconMaxEntries
    print

    # Scan the lexicon (unordered), printing some of the data
    # using Standard Format markers.
    # (Uses a slice to only print a portion.)
    for e in list(project.LexiconAllEntries())[:LexiconMaxEntries]:
        print "\lx", project.LexiconGetLexemeForm(e)
        print "\lc", project.LexiconGetCitationForm(e)
        for sense in e.SensesOS :
            print "\ge", project.LexiconGetSenseGloss(sense)
            print "\pos", project.LexiconGetSensePOS(sense)
            print "\def", project.LexiconGetSenseDefinition(sense)
            if WriteTests and ftflagsFlid:
                flags = project.LexiconGetFieldText(sense, ftflagsFlid)
                print "FTFlags", flags
                if flags:
                    project.LexiconAddTagToField(sense, ftflagsFlid, "tag-1")
                else:
                    project.LexiconSetFieldText(sense, ftflagsFlid, u"FLAG!")
                flags = project.LexiconGetFieldText(sense, ftflagsFlid)
                print "New FTFlags", flags
            if WriteTests:
                if project.LexiconGetSenseGloss(sense) == u"Example Gloss":
                    project.LexiconSetSenseGloss(sense, u"Changed Gloss")
                print "New Gloss", project.LexiconGetSenseGloss(sense)

            for example in sense.ExamplesOS:
                ex = project.LexiconGetExample(example)
                print "\ex", ex
                if WriteTests and not ex:
                    # CHANGES the DB
                    print "Setting example"
                    project.LexiconSetExample(example,
                                             "You should have an example sentence"
                                             )

        print


#--------------------------------------------------------------------


if __name__ == "__main__":

    FLExInit.Initialize()
    
    project = FLExProject()

    try:
        project.OpenProject(projectName = projectName,
                            writeEnabled = WriteTests,
                            verbose = True)
    except FDA_ProjectError, e:
        print "LCM Cache Create failed!"
        print e.message

    reportLexicalEntries(project)
    
    FLExInit.Cleanup()
    
    