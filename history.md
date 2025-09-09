# flexlibs History

## Known Issues

None

## History

### 1.2.8 - 10 Sep 2025

+ FLExProject functions:
    + Added LexiconClearListFieldSingle() 
    + Added LexiconSetLexemeForm()
    + Added LexiconGetExampleCustomFields()
    + Added LexiconGetAllomorphCustomFields()

### 1.2.7 - 25 Aug 2025

+ Supports Python 3.8 - 3.13
+ Supports FieldWorks 9.0.17 - 9.3.1

+ FLExProject functions:
    + Added GetFieldID()
    + Added support for Lists (single or multiple) in GetCustomFieldValue()
    + Added ListFieldPossibilityList()
    + Added ListFieldPossibilities()
    + Added ListFieldLookup()
    + Added LexiconSetListFieldSingle() 
    + Added LexiconSetListFieldMultiple() 

### 1.2.6 - 26 Jun 2025

+ Supports Python 3.8 - 3.13
+ Supports FieldWorks 9.0.17 - 9.2.8

### 1.2.5 - 13 Jun 2025

+ When generating the list of projects, check that the fwdata file 
  exists, not just the directory. [Issue #14]
+ New function:
    + OpenProjectInFW(projectName)
+ Tidied up the presentation of the API documentation.

### 1.2.4 - 14 Aug 2024

+ New FLExProject function:
    + ObjectRepository(repository)

### 1.2.3 - 9 Jul 2024

+ GetAllSemanticDomains() returns ICmSemanticDomain objects
+ New FLExProject functions:
    + Object(hvoOrGuid)
    + LexiconAllEntriesSorted()
    + GetLexicalRelationTypes()
    + GetPublications()
    + PublicationType(publicationName)

### 1.2.2 - 15 Nov 2023

+ Supports Python 3.8 - 3.12
+ Supports FieldWorks 9.0.4 - 9.1.25

### 1.2.1 - 29 Aug 2023

+ Supports Python 3.6 - 3.11
+ Supports FieldWorks 9.0.4 - 9.1.22

+ New FLExProject functions:
    + LexiconFieldIsMultiType() 
    + LexiconFieldIsAnyStringType()
    + LexiconGetSenseNumber()
    + LexiconSenseAnalysesCount()

### 1.2.0 - 16 Aug 2023

+ Moved to pythonnet 3.0.1, which supports FieldWorks 9.1.22

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
  