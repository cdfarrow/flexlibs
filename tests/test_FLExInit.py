from unittest import TestCase
from flexlibs import FLExInit


class TestFLExInit(TestCase):
    def test_InitializeCleanup(self):
        try:
            FLExInit.Initialize()
        except:
            self.fail("Failed to initialize")
        try:
            FLExInit.Cleanup()
        except:
            self.fail("Failed to Cleanup")
