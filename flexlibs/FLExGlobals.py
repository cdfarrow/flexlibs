#
#   FLExGlobals.py
#
#   Module: Fieldworks Language Explorer path initialisation.
#
#           This module sets up the path for import of the 
#           Fieldworks Assemblies.
#
#   Platform: Python.NET & IRONPython
#
#   Copyright Craig Farrow, 2011 - 2018
#

import sys
import os
import glob
import shutil

import clr
import System
clr.AddReference("System.Data")

from System import Environment

# FW9 TODO : change to using .NET registry API
clr.AddReference("mscorlib")        # Where Win32 assembly resides
from Microsoft.Win32 import Registry, RegistryKey


#----------------------------------------------------------------
# Fieldworks registry constants

FWRegKeys = { "9" : r"SOFTWARE\SIL\Fieldworks\9" }

FWRegCodeDir = "RootCodeDir"
FWRegProjectsDir = "ProjectsDir"

#----------------------------------------------------------------
def GetFWRegKey(fwVersion):

    try:
        RegKey = FWRegKeys[fwVersion]
    except KeyError:
        raise Exception("Error: Unsupported Fieldworks version (%s)" % fwVersion)

    rKey = Registry.CurrentUser.OpenSubKey(RegKey)
    print "GetFWRegKey: CurrentUser = ", rKey
    if rKey and rKey.GetValue(FWRegCodeDir):
        return rKey
        
    rKey = Registry.LocalMachine.OpenSubKey(RegKey)
    print "GetFWRegKey: LocalMachine = ", rKey
    if rKey and rKey.GetValue(FWRegCodeDir):
        return rKey

    return None

# -------------------------------------------------------------------

def InitialiseFWGlobals():
    global FWCodeDir
    global FWProjectsDir
    global FWMajorVersion
    global FWShortVersion
    global FWLongVersion

    # FW9 TODO -- 32bit exec doesn't find 64bit FW in registry
    #               (it looks in WOW6432Node)
    # # The environment variable FWVersion is configured by py_net.bat to 
    # # tell us which version of the FW DLLs we are running with 
    # # (so we know which path to use for FW libraries.)
    try:
        FWMajorVersion = os.environ["FWVersion"]
    except KeyError:
        raise Exception("Error: FWVersion environment variable not defined!")

    # print "Startup: py_net.bat set FwVersion =", FWMajorVersion
    # rKey = GetFWRegKey(FWMajorVersion)
    # if not rKey:
        # raise Exception("Can't find Fieldworks %s!" % FWMajorVersion)

    # codeDir = rKey.GetValue(FWRegCodeDir)
    # projectsDir = rKey.GetValue(FWRegProjectsDir)

    # print "Startup: Reg codeDir =", codeDir
    # print "Startup: Reg projectsDir =", projectsDir

    # # On developer's machines we also check the build directories for FieldWorks.exe

    # if not os.access(os.path.join(codeDir, "FieldWorks.exe"), os.F_OK):
        # if os.access(os.path.join(codeDir, r"..\Output\Release\FieldWorks.exe"), os.F_OK):
            # codeDir = os.path.join(codeDir, r"..\Output\Release")
        # elif os.access(os.path.join(codeDir, r"..\Output\Debug\FieldWorks.exe"), os.F_OK):
            # codeDir = os.path.join(codeDir, r"..\Output\Debug")
        # else:
            # raise Exception("Error: Can't find path for FieldWorks.exe.")
        
    # FW9 TODO - dynamically find the paths
    FWCodeDir       = r"C:\Program Files (x86)\SIL\FieldWorks 9" #codeDir
    FWProjectsDir   = r"C:\ProgramData\SIL\FieldWorks\Projects" #projectsDir

    print "FLExGlobals: FWCodeDir =", FWCodeDir
    print "FLExGlobals: FWProjectsDir =", FWProjectsDir
    

    # Add the FW code directory to the search path for importing FW libs.
    sys.path.append(FWCodeDir)
    
    print "FLExGlobals: sys.path ="
    for x in sys.path: print "\t", x

    # These can't be imported until the path is set:
    clr.AddReference("FwUtils")
    from SIL.FieldWorks.Common.FwUtils import VersionInfoProvider
    from System.Reflection import Assembly

    # Get the full version information out of FW itself
    vip = VersionInfoProvider(Assembly.GetAssembly(VersionInfoProvider), False)
    FWShortVersion = System.Version(vip.ShortNumericAppVersion) # e.g. 8.1.3
    FWLongVersion = vip.ApplicationVersion
    print "FLExGlobals: FWShortVersion =", FWShortVersion
    print "FLExGlobals: FWLongVersion =", FWLongVersion
    
