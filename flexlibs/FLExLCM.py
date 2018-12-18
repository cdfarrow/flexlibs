#
#   FLExLCM.py
#
#   Module:     Project access functions for FieldWorks Language Explorer
#               via SIL Language and Culture Model (LCM).
#               (Prior to FW 9 this was known as "FDO" -- "FieldWorks
#               Data Objects")
#
#   Platform: Python.NET
#             (ITsString doesn't work in IRONPython)
#             FieldWorks Version 9
#
#   Copyright Craig Farrow, 2008 - 2018
#

import os

import clr
clr.AddReference("System")
import System

clr.AddReference("FwUtils")
clr.AddReference("FieldWorks")
clr.AddReference("FwCoreDlgs")
clr.AddReference("FwControls")
clr.AddReference("FdoUi")
clr.AddReference("SIL.Core")
clr.AddReference("SIL.Core.Desktop")
clr.AddReference("SIL.LCModel")
clr.AddReference("SIL.LCModel.Core")

# Classes needed for loading the Cache
from SIL.LCModel import LcmCache, LcmSettings, LcmFileHelper
from SIL.LCModel.Core.Text import Icu
from SIL.LCModel.Core.Cellar import CellarPropertyType

from SIL.FieldWorks import ProjectId
from SIL.FieldWorks.Common.Controls import ProgressDialogWithTask
from SIL.FieldWorks.Common.FwUtils import ThreadHelper
from SIL.FieldWorks.Common.FwUtils import FwDirectoryFinder
from SIL.FieldWorks.Common.FwUtils import FwUtils
from SIL.FieldWorks.FdoUi import FwLcmUI
from SIL.FieldWorks.FwCoreDlgs import ChooseLangProjectDialog


#--- Globals --------------------------------------------------------

CellarStringTypes  = (CellarPropertyType.String, )
CellarUnicodeTypes = (CellarPropertyType.MultiUnicode,
                      CellarPropertyType.MultiString)

#-----------------------------------------------------------

def GetListOfProjects():
    # TODO: Use FW Project Chooser (ChooseLangProjectDialog())
    #       and handle network drives
    projectsPath = FwDirectoryFinder.ProjectsDirectory
    objs = os.listdir(unicode(projectsPath))
    projectList = []
    for f in objs:
        if os.path.isdir(os.path.join(projectsPath, f)):
            projectList.append(f)
    return sorted(projectList)

#-----------------------------------------------------------

def OpenProject(projectName, writeEnabled = False, allowMigration = False):
    """
    Open the project given by projectName:
        - Either the full path including ".fwdata" suffix, or
        - The name only, opened from the default project location.

    writeEnabled : (Awaiting FW support for a read-only mode so that
                    FW doesn't have to be closed for read-only operations.)
    allowMigration : Set this to True to prevent project migration;
                     otherwise, a project in an old format will be
                     automatically migrated to the lastest version.
    """

    projectFileName = LcmFileHelper.GetXmlDataFileName(projectName)

    #print "FLExLCM.OpenProject:", projectFileName

    projId = ProjectId(projectFileName)

    th = ThreadHelper()
    ui = FwLcmUI(None, th)     # IHelpTopicProvider, ISynchronizeInvoke
    dirs = FwDirectoryFinder.LcmDirectories
    settings = LcmSettings()
    settings.DisableDataMigration = not allowMigration

    dlg = ProgressDialogWithTask(th)

    # SIL.LCModel\LcmCache.cs
    # public static LcmCache CreateCacheFromExistingData(
    #    IProjectIdentifier projectId,
    #    string userWsIcuLocale,
    #    ILcmUI ui,
    #    ILcmDirectories dirs,
    #    LcmSettings settings,
    #    IThreadedProgress progressDlg)

    return LcmCache.CreateCacheFromExistingData(projId,
                                                "en",
                                                ui,
                                                dirs,
                                                settings,
                                                dlg)
