#----------------------------------------------------------------------------
# Name:         flexlibs
# Purpose:      This package provides a Python interface to FLEx project data 
#               via the Fieldworks Language and Culture Model (LCM).
#----------------------------------------------------------------------------

version = "1.2.8"

# Define exported classes, etc. at the top level of the package

from .code.FLExInit import (
    FLExInitialize, 
    FLExCleanup,
    )
    
from .code.FLExGlobals import (
    FWCodeDir, 
    FWProjectsDir, 
    FWExecutable,
    FWShortVersion, 
    FWLongVersion,
    APIHelpFile,
    )

from .code.FLExProject import (
    AllProjectNames,
    OpenProjectInFW,
    FLExProject,
    FP_FileLockedError,
    FP_FileNotFoundError,
    FP_MigrationRequired, 
    FP_NullParameterError, 
    FP_ParameterError, 
    FP_ProjectError, 
    FP_ReadOnlyError, 
    FP_RuntimeError, 
    FP_WritingSystemError,
    )
