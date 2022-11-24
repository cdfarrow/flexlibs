# flexlibs History

## Known Issues

* pythonnet 3.0 has been released, but flexlibs hasn't been updated to work with it yet.
* Requires Python <= 3.8 due to pythonnet's requirements.

## History

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
  