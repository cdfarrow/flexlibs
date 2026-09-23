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
FWExecutable = None
FWShortVersion = None
FWLongVersion = None

# (Double dirname() goes up a directory)
APIHelpFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                           r"docs\flexlibsAPI\flexlibs.html")

# ----------------------------------------------------------------
# FieldWorks registry constants

FW_SUPPORTED_VERSIONS = ["9"]
FWREG_CODEDIR       = "RootCodeDir"
FWREG_PROJECTSDIR   = "ProjectsDir"

FWRegKeys = { 
                "9" : r"SOFTWARE\SIL\FieldWorks\9",
            }

# Env overrides (CI / no-installer layouts). Checked before registry.
ENV_FW_CODE_DIR = "FLEXLIBS_FW_CODE_DIR"
ENV_FW_PROJECTS_DIR = "FLEXLIBS_FW_PROJECTS_DIR"
ENV_ASSEMBLY_DIR = "FLEXLIBS_ASSEMBLY_DIR"


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

def _resolveCodeDirFromRegistry(rKey):
    if platform.system() == "Linux":
        # **********************************************************
        # TODO: First attempt at Linux support. 
        # As of Apr2024, FW installation has changed to use flatpak
        # and this no longer works.
        # **********************************************************
        # On Linux, for installed versions of Flex,
        # FWREG_CODEDIR points to /usr/share/fieldworks,
        # but FieldWorks.exe resides in /usr/lib/fieldworks.
        # I can't find any registry keys/values that point to
        # the correct location.
        # For installed version, the app calls /bin/fieldworks-flex
        # from /usr/share/applications/fieldworks-applicatoins.desktop,
        # which in turn calls /usr/lib/fieldworks/run-app FieldWorks.exe etc.
        #
        # The following is based on the logic in /usr/lib/fieldworks/environ
        codeDir = os.path.join(rKey.GetValue(FWREG_CODEDIR), "../../lib/fieldworks")
    else:
        # On windows, FWREG_CODEDIR is correct.
        codeDir = rKey.GetValue(FWREG_CODEDIR)

    if not os.access(os.path.join(codeDir, "FieldWorks.exe"), os.F_OK):
        # On developer's machines we also check the build directories 
        # for FieldWorks.exe
        if platform.system() == "Linux":
            devPaths = [
                os.path.dirname(rKey.GetValue(FWREG_CODEDIR)),
                ]
        else:
            # Windows
            devPaths = [
                os.path.join(codeDir, r"..\Output\Release\\"),
                os.path.join(codeDir, r"..\Output\Debug\\"),
                ]

        for p in devPaths:
            if os.access(os.path.join(p, "FieldWorks.exe"), os.F_OK):
                return p

        msg = "FieldWorks.exe not found in %s" % codeDir
        logger.error(msg)
        raise Exception(msg)

    return codeDir


def _resolvePathsFromEnv():
    """
    Resolve FWCodeDir / FWProjectsDir from FLEXLIBS_* env vars.
    Returns (codeDir, projectsDir) or None if FLEXLIBS_FW_CODE_DIR is unset.
    """
    codeDir = os.environ.get(ENV_FW_CODE_DIR)
    if not codeDir:
        return None

    codeDir = os.path.abspath(codeDir)
    if not os.path.isdir(codeDir):
        raise Exception("%s is not a directory: %s" % (ENV_FW_CODE_DIR, codeDir))
    if not os.access(os.path.join(codeDir, "FieldWorks.exe"), os.F_OK):
        raise Exception("FieldWorks.exe not found in %s=%s" % (ENV_FW_CODE_DIR, codeDir))

    projectsDir = os.environ.get(ENV_FW_PROJECTS_DIR)
    if not projectsDir:
        raise Exception(
            "%s is set but %s is missing (required for env-based discovery)"
            % (ENV_FW_CODE_DIR, ENV_FW_PROJECTS_DIR))

    projectsDir = os.path.abspath(projectsDir)
    if not os.path.isdir(projectsDir):
        raise Exception("%s is not a directory: %s" % (ENV_FW_PROJECTS_DIR, projectsDir))

    logger.info("Using FieldWorks paths from environment")
    return codeDir, projectsDir


def _applyAssemblyOverlay():
    """
    If FLEXLIBS_ASSEMBLY_DIR is set, prepend it to sys.path so NuGet
    (or other) DLLs shadow copies from the FieldWorks code directory.
    """
    overlayDir = os.environ.get(ENV_ASSEMBLY_DIR)
    if not overlayDir:
        return None

    overlayDir = os.path.abspath(overlayDir)
    if not os.path.isdir(overlayDir):
        raise Exception("%s is not a directory: %s" % (ENV_ASSEMBLY_DIR, overlayDir))

    dlls = [f for f in os.listdir(overlayDir) if f.lower().endswith(".dll")]
    if not dlls:
        raise Exception("%s contains no DLLs: %s" % (ENV_ASSEMBLY_DIR, overlayDir))

    sys.path.insert(0, overlayDir)
    logger.info("Assembly overlay active: %s (%d DLLs)" % (overlayDir, len(dlls)))
    return overlayDir


def InitialiseFWGlobals():
    global FWCodeDir
    global FWProjectsDir
    global FWExecutable
    global FWShortVersion
    global FWLongVersion

    envPaths = _resolvePathsFromEnv()
    if envPaths:
        FWCodeDir, FWProjectsDir = envPaths
    else:
        try:
            rKey = GetFWRegKey()
        except Exception as e:
            logging.exception("Couldn't find FieldWorks registry entry")
            raise

        FWCodeDir = _resolveCodeDirFromRegistry(rKey)
        # FWREG_PROJECTSDIR is correct on Windows and Linux.
        FWProjectsDir = rKey.GetValue(FWREG_PROJECTSDIR)
        logger.info("Using FieldWorks paths from registry")

    FWExecutable = os.path.join(FWCodeDir, "FieldWorks.exe")

    # Optional NuGet/other overlay first, then the FieldWorks code dir.
    _applyAssemblyOverlay()
    sys.path.append(FWCodeDir)

    logger.info("sys.path = \n\t%s" % "\n\t".join(sys.path))

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

    # When overlaying NuGet packages, log where a key SIL assembly loaded from.
    try:
        clr.AddReference("SIL.LCModel")
        from SIL.LCModel import LcmCache
        lcmAsm = Assembly.GetAssembly(LcmCache)
        logger.info("SIL.LCModel loaded from %s" % lcmAsm.Location)
    except Exception:
        logger.debug("Could not report SIL.LCModel load location", exc_info=True)
