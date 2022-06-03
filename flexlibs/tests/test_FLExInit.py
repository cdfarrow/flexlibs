import unittest
from flexlibs import FLExInitialize, FLExCleanup


class TestFLExInit(unittest.TestCase):
    def test_InitializeCleanup(self):
        try:
            FLExInitialize()
        except:
            self.fail("Failed to initialize")
        try:
            FLExCleanup()
        except:
            self.fail("Failed to Cleanup")


if __name__ == "__main__":
    unittest.main()
