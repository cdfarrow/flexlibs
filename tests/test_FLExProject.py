from unittest import TestCase
from flexlibs import FLExInit
from flexlibs.FLExProject import FLExProject


class TestFLExProject(TestCase):
    @classmethod
    def setUpClass(cls):
        FLExInit.Initialize()
        cls.project = FLExProject()

    @classmethod
    def tearDownClass(cls):
        FLExInit.Cleanup()

    def test_GetProjectNames(self):
        self.assertIsInstance(self.project.GetProjectNames(), list)

    def test_OpenProject(self):
        pass
