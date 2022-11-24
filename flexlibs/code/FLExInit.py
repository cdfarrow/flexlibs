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

import logging
logger = logging.getLogger(__name__)


from .. import version
logger.info("flexlibs version: %s" % version)

# Python version check:
# (pythonnet 2.5 doesn't support beyond Python 3.8; pythonnet 3 is in 
# Alpha -- May2022)
PYTHON_MAX_VERSION = (3, 8)

logger.info("Python version: %s" % sys.version)
if sys.version_info[0:2] > PYTHON_MAX_VERSION:
    raise Exception('Sorry, Python versions greater than %d.%d are not yet supported' % PYTHON_MAX_VERSION)


import clr

# Configure the path for accessing the FW DLLs
from . import FLExGlobals
FLExGlobals.InitialiseFWGlobals() 


# This is a workaround to redirect the dll loading to old versions of 
# dlls that are still needed by some FLEx libraries. FLEx handles it via 
# a redirect in its .config file, but we don't have one of those with 
# FLExTools. When FLEx updates the dlls again, simply drop the *old* dll 
# into the flex-dlls\ folder.

lib_path = os.path.join(os.path.dirname(__file__), 
                        r"..\flex-dlls\*.dll")
 
for dll in glob.glob(lib_path):
    dll_path = os.path.abspath(dll)
    logger.debug("".join(("Adding Reference to local dll: ", dll_path)))
    clr.AddReference(dll_path)


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
