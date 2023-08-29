# flexlibs History

## Known Issues

None

## History

### 1.2.1 - 29 Aug 2023

+ Supports Python 3.6 - 3.11
+ Supports FieldWorks 9.0.4 - 9.1.22
    
+ New functions:
    + LexiconFieldIsMultiType() 
    + LexiconFieldIsAnyStringType()
    + LexiconGetSenseNumber()
    + LexiconSenseAnalysesCount()

### 1.2.0 - 16 Aug 2023

+ Moved to pythonnet 3.0.1, which supports:

+ FieldWorks dlls no longer need to be included, so the package size 
  has been greatly reduced.

### 1.1.8 - 11 Apr 2023

+ Added LexiconClearField()
+ Updated Set/Get Field functions to handle MultiStrings and a WS 
  parameter (fully backward compatible).

### 1.1.6 - 24 Nov 2022

+ Added the DLLs needed to support FieldWorks 9.1.15/16
+ Added support for Texts to BuildGotoURL()

### 1.1.5 - 15 Oct 2022

+ Constrained pythonnet to < 3 since flexlibs breaks with the new v3.0.0 

### 1.1.3 - 24 Jun 2022

+ FLExProject now requires a CloseProject() call to save data and
  release the lock on the FLEx project.

### 1.1.2 - 20 Jun 2022

+ Configured as a package and published on PyPI
+ Includes .NET DLLs that are needed for compatibility with FLEx 9.0
  through to 9.1.9
  