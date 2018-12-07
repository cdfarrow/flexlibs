#
#   FLExInit.py
#
#   Module: Fieldworks Language Explorer initialisation.
#
#   Note:   This module needs to be imported before importing or
#           using any Fieldworks Assemblies as it sets up the
#           path, and other low-level things.
#
#   Usage:  Call Initialize() and Cleanup() from the main application.
#
#   Platform: Python.NET & IRONPython
#             FieldWorks Version 9
#
#   Copyright Craig Farrow, 2011 - 2018
#

import sys
import os
import glob
import shutil

import clr

# Configure the path for accessing the FW DLLs
import FLExGlobals     
FLExGlobals.InitialiseFWGlobals() 

clr.AddReference("FwUtils")
from SIL.FieldWorks.Common.FwUtils import FwRegistryHelper, FwUtils
clr.AddReference("SIL.WritingSystems")
from SIL.WritingSystems import Sldr


# -------------------------------------------------------------------

def Initialize ():

    # [FW9] These 3 inits copied from LCMBrowser::Main()
    FwRegistryHelper.Initialize()
    FwUtils.InitializeIcu()
    # No need to access internet SLDR: Offline mode = True 
    Sldr.Initialize(True)   


def Cleanup():

    Sldr.Cleanup();

