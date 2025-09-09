from builtins import str

import unittest

from flexlibs import FLExInitialize, FLExCleanup
from flexlibs import FLExProject, AllProjectNames, FP_FileLockedError

# --- Constants ---

TEST_PROJECT = r"__flexlibs_testing"
CUSTOM_FIELD = r"EntryFlags"
CUSTOM_VALUE = r"Test.Value"

#----------------------------------------------------------- 

class TestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        FLExInitialize()

    @classmethod
    def tearDownClass(self):
        FLExCleanup()

    def _openProject(self):
        fp = FLExProject()
        try:
            fp.OpenProject(TEST_PROJECT,
                           writeEnabled = True)
        except FP_FileLockedError:
            self.fail("The test project is open in another application. Please close it and try again.")

        except Exception as e:
            self.fail("Exception opening project %s:\n%s" % 
                      (TEST_PROJECT, e.Message))
        return fp

    def _closeProject(self, fp):
        fp.CloseProject()

    def test_WriteFields(self):
        fp = self._openProject()
        flags_field = fp.LexiconGetEntryCustomFieldNamed(CUSTOM_FIELD)
        if not flags_field:
            self.fail("Entry-level custom field named '%s' not found." % CUSTOM_FIELD)
            
        # Traverse the whole lexicon
        for lexEntry in fp.LexiconAllEntries():
            self.assertIsInstance(fp.LexiconGetHeadword(lexEntry), str)
            try:
                fp.LexiconSetFieldText(lexEntry, flags_field, CUSTOM_VALUE)
            except Exception as e:
                self.fail("Exception writing custom field %s:\n%s" % 
                            (CUSTOM_FIELD, e.Message))

        # Read back and check that the values were written.
        for lexEntry in fp.LexiconAllEntries():
            value = fp.LexiconGetFieldText(lexEntry, flags_field)
            self.assertEqual(value, CUSTOM_VALUE)

        # Clear the field again
        for lexEntry in fp.LexiconAllEntries():
            fp.LexiconSetFieldText(lexEntry, flags_field, "")
                
        self._closeProject(fp)
    
if __name__ == "__main__":
    unittest.main()
