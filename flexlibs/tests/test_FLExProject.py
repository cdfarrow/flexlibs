from builtins import str

import unittest

import logging
logging.basicConfig(filename='flexlibs.log', filemode='w', level=logging.DEBUG)

from flexlibs import FLExInitialize, FLExCleanup
from flexlibs import FLExProject, AllProjectNames

class TestFLExProject(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        FLExInitialize()

    @classmethod
    def tearDownClass(self):
        FLExCleanup()

    def test_AllProjectNames(self):
        self.assertIsInstance(AllProjectNames(), list)

    def test_OpenProject(self):
        fp = FLExProject()
        # Grab the first project in the list
        projectName = AllProjectNames()[0]
        try:
            fp.OpenProject(projectName,
                           writeEnabled = False)
        except Exception as e:
            self.fail("Exception opening project %s:\n%s" % 
                        (projectName, e.message))
        fp.CloseProject()

    def test_ReadLexicon(self):
        fp = FLExProject()
        projectName = AllProjectNames()[0]
        try:
            fp.OpenProject(projectName,
                           writeEnabled = False)
        except Exception as e:
            self.fail("Exception opening project %s" % projectName)

        # Traverse the whole lexicon
        for lexEntry in fp.LexiconAllEntries():
            self.assertIsInstance(fp.LexiconGetHeadword(lexEntry), str)

        fp.CloseProject()



if __name__ == "__main__":
    unittest.main()
