import unittest

import logging
logging.basicConfig(filename='flexlibs.log', filemode='w', level=logging.DEBUG)

from flexlibs import FLExInit
from flexlibs.FLExProject import FLExProject, GetProjectNames

class TestFLExProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        FLExInit.Initialize()
        cls.project = FLExProject()

    @classmethod
    def tearDownClass(cls):
        FLExInit.Cleanup()

    def test_GetProjectNames(self):
        self.assertIsInstance(GetProjectNames(), list)

    def test_OpenProject(self):
        fp = FLExProject()
        projectName = GetProjectNames()[0]
        try:
            fp.OpenProject(projectName,
                           writeEnabled = False)
        except Exception as e:
            del fp
            self.fail("Exception opening project %s:\n%s" % 
                        (projectName, e.message))

    def test_ReadLexicon(self):
        fp = FLExProject()
        projectName = GetProjectNames()[0]
        try:
            fp.OpenProject(projectName,
                           writeEnabled = False)
        except Exception as e:
            del fp
            self.fail("Exception opening project %s" % projectName)

        # Traverse the whole lexicon
        for lexEntry in fp.LexiconAllEntries():
            self.assertIsInstance(fp.LexiconGetHeadword(lexEntry), str)



if __name__ == "__main__":
    unittest.main()
