import unittest
from flexlibs import FLExInit


class TestFLExInit(unittest.TestCase):
    def test_InitializeCleanup(self):
        try:
            FLExInit.Initialize()
        except:
            self.fail("Failed to initialize")
        try:
            FLExInit.Cleanup()
        except:
            self.fail("Failed to Cleanup")


if __name__ == "__main__":
    unittest.main()
