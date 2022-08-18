#
#   FLExGlobals.py
#
#   Module: FieldWorks Language Explorer path initialisation.
#
#           This module sets up the path for import of the 
#           FieldWorks Assemblies.
#
#   Platform: Python.NET & IRONPython
#             FieldWorks Version 9.0, 9.1
#
#   Copyright Craig Farrow, 2011 - 2022
#

import sys
import os
import platform
import glob
import shutil

import clr
import System

clr.AddReference("System.Data")

from System import Environment
from System.Reflection import Assembly
from Microsoft.Win32 import Registry, RegistryKey

import logging
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------
# Public globals

FWCodeDir = None
FWProjectsDir = None
FWShortVersion = None
FWLongVersion = None

# (Double dirname() goes up a directory)
APIHelpFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                           r"docs\flexlibsAPI\index.html")

# ----------------------------------------------------------------
# FieldWorks registry constants

FW_SUPPORTED_VERSIONS = ["9"]
FWREG_CODEDIR       = "RootCodeDir"
FWREG_PROJECTSDIR   = "ProjectsDir"

FWRegKeys = { 
                "9" : r"SOFTWARE\SIL\FieldWorks\9",
            }


# ----------------------------------------------------------------
def GetFWRegKey():
    logger.info(".NET version: %s" % Environment.Version)

    # Note: The registry looks up 32bit (via WOW3264Node) if we are 
    # running 32 bit Python, so no need for special handling. 

    python32or64 = platform.architecture()[0]   # "32bit"/"64bit"

    for fwVersion in FW_SUPPORTED_VERSIONS:
        logger.info("Looking for FieldWorks %s, %s..." \
                     % (fwVersion, python32or64))

        RegKey = FWRegKeys[fwVersion]
        rKey = Registry.CurrentUser.OpenSubKey(RegKey)
        logger.info("GetFWRegKey: %s => %s" % (RegKey, rKey))
        if rKey and rKey.GetValue(FWREG_CODEDIR):
            return rKey

        rKey = Registry.LocalMachine.OpenSubKey(RegKey)
        logger.info("GetFWRegKey: %s => %s" % (RegKey, rKey))
        if rKey and rKey.GetValue(FWREG_CODEDIR):
            return rKey

    msg = "%s FieldWorks %s not found" \
            % (python32or64, " or ".join(FW_SUPPORTED_VERSIONS))
    raise Exception(msg)


# -------------------------------------------------------------------

def InitialiseFWGlobals():
    global FWCodeDir
    global FWProjectsDir
    global FWShortVersion
    global FWLongVersion

    try:
        rKey = GetFWRegKey()
    except Exception as e:
        logging.exception("Couldn't find FieldWorks registry entry")
        raise

    if platform.system() == "Linux":
        # On Linux, for installed versions of Flex,
        # FWREG_CODEDIR points to /usr/share/fieldworks,
        # but FieldWorks.exe resides in /usr/lib/fieldworks.
        # I can't find any registry keys/values that point to
        # the correct location.
        # For installed version, the app calls /bin/fieldworks-flex
        # from /usr/share/applications/fieldworks-applicatoins.desktop,
        # which in turn calls /usr/lib/fieldworks/run-app FieldWorks.exe etc.
        #
        # I'm not sure what to do with developer versions on Linux.
        FWCodeDir = "/usr/lib/fieldworks"
    else:
        # On windows, FWREG_CODEDIR is correct.
        FWCodeDir = rKey.GetValue(FWREG_CODEDIR)

    # FWREG_PROJECTSDIR is correct on Windows and Linux.
    FWProjectsDir = rKey.GetValue(FWREG_PROJECTSDIR)

    # On developer's machines we also check the build directories 
    # for FieldWorks.exe

    if not os.access(os.path.join(FWCodeDir, "FieldWorks.exe"), os.F_OK):
        if os.access(os.path.join(FWCodeDir, r"..\Output\Release\FieldWorks.exe"), os.F_OK):
            FWCodeDir = os.path.join(FWCodeDir, r"..\Output\Release")
        elif os.access(os.path.join(FWCodeDir, r"..\Output\Debug\FieldWorks.exe"), os.F_OK):
            FWCodeDir = os.path.join(FWCodeDir, r"..\Output\Debug")
        else:
            # This can happen if there is a ghost registry entry for 
            # an uninstalled FLEx
            msg = "FieldWorks.exe not found in %s" \
                            % FWCodeDir
            logger.error(msg)
            raise Exception(msg)

    # Add the FW code directory to the search path for importing FW libs.
    sys.path.append(FWCodeDir)

    logger.info("sys.path = %s" % "\n\t".join(sys.path))

    # These can't be imported until the path is set:
    clr.AddReference("FwUtils")
    from SIL.FieldWorks.Common.FwUtils import VersionInfoProvider

    # Get the full version information out of FW itself
    vip = VersionInfoProvider(Assembly.GetAssembly(VersionInfoProvider), False)
    FWShortVersion = System.Version(vip.ShortNumericAppVersion)  # e.g. 8.1.3
    FWLongVersion = vip.ApplicationVersion

    logger.info("Found FieldWorks installation")
    logger.info("FWCodeDir = %s" % FWCodeDir)
    logger.info("FWProjectsDir = %s" % FWProjectsDir)
    logger.info("FWShortVersion = %s" % FWShortVersion)
    logger.info("FWLongVersion = %s" % FWLongVersion)
