#
#   FLExInit.py
#
#   Module: Fieldworks Language Explorer initialisation.
#
#   Note:   This module needs to be imported before importing or
#           using any Fieldworks Assemblies as it sets up the
#           path, and other low-level things.
#
#   Usage:  Call FLExInitialize() and FLExCleanup() as the first and 
#           last actions from the main application.
#
#   Platform: Python.NET & IRONPython
#             FieldWorks Version 9
#
#   Copyright Craig Farrow, 2011 - 2022
#

import sys
import os
import glob
import shutil
import platform

import logging
logger = logging.getLogger(__name__)


from .. import version
logger.info("flexlibs version: %s" % version)

logger.info("Python version: %s" % sys.version)


import clr

# Configure the path for accessing the FW DLLs
from . import FLExGlobals
FLExGlobals.InitialiseFWGlobals() 


clr.AddReference("FwUtils")
from SIL.FieldWorks.Common.FwUtils import FwRegistryHelper, FwUtils
clr.AddReference("SIL.WritingSystems")
from SIL.WritingSystems import Sldr


# -------------------------------------------------------------------

def FLExInitialize ():
    """
    Initialize the Fieldworks libraries. An application should call
    this as the first thing it does.
    """
    # [FW9] These 3 inits copied from LCMBrowser::Main()
    logger.debug("Calling RegistryHelper.Initialize()")
    FwRegistryHelper.Initialize()
    logger.debug("Calling InitializeIcu()")
    if platform.system() == "Linux":
        from Icu import Wrapper #, VersionInfo
        # The Flex beta on Linux currently ships with a version of ICU
        # that has a minor version (54.1), but Icu.Net can only handle 
        # finding a version of ICU that can be parsed as an integer. 
        # The beta also ships with the version 54 libraries, but 
        # Icu.Net can't find it because it finds 54.1 first and then 
        # fails.
        # I'm not sure what exactly FieldWorks does to address this, 
        # but limiting the version here works.
        Wrapper.ConfineIcuVersions(54,54)
    FwUtils.InitializeIcu()
    # No need to access the online SLDR: Offline mode = True
    logger.debug("Calling Sldr.Initialize()")
    Sldr.Initialize(True)
    # Sldr.Initialize() can fail silently. If it doesn't return, 
    # then it is likely a dll issue.
    logger.debug("FLExInit.Initialize complete")


def FLExCleanup():
    """
    Close up the Fieldworks libraries. An application should call this
    before exiting.
    """
    Sldr.Cleanup();
