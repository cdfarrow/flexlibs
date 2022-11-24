Background:
-----------

From time to time Fieldworks updates the version of third-party dlls 
that it includes in its installation, even though not all Fieldworks 
libraries are updated to use the new version. This discrepancy is 
handled with a (version) redirection in the Fieldworks.exe.config 
file. Other applications, such as Phonology Assistant include the 
later versions, and also use redirection in the .config file.

Because FlexTools is a Python application, we can't easily use a 
.config file. Setuptools can create a simple wrapper exe that calls 
Python, however, we would still need to supply a config file in the
same location, and (automatically?) update the config file when the 
FLEx .config file changes.

The alternative is to include the old dlls in the FlexTools 
installation. This is the current solution. All dlls in this folder are 
loaded (in FlexInit.py) with clr.AddReference(). clr keeps track of 
multiple versions, so we can keep putting new versions of the dlls here 
as needed while maintaining backward compatibility with older versions 
of Fieldworks.

The Fieldworks dlls that affect FlexTools are:
    FwUtils             --> icu.net.dll
    SIL.Core            -->              Newtonsoft.JSON.dll
    SIL.WritingSystems  --> icu.net.dll; Newtonsoft.JSON.dll

----------------------------------------------------------- 
History:
--------

Fieldworks 9.0.8 installs v12 of Newtonsoft.JSON.dll.
--> v11 from FW 9.0.7 is included here.

Fieldworks 9.1.9 installs v2.8 of icu.net.dll
--> v2.7 from FW 9.1.8 is included here along with 
Microsoft.Extensions.DependencyModel.dll (v2.0), which is referenced 
by icu.net.dll.

Fieldworks  | icu.net   | Newtonsoft  | FWUtils/Core/WritingSystems
----------------------------------------------------------- 
9.0.7       |   2.7     |   11       
9.0.8       |   2.7     |   12
    >> FlexTools 2.1.1:  Includes 2.7 & 11
9.0.17      |   2.7     |   12 << Latest "Stable Release"
9.1.8       |   2.7     |   12
9.1.9       |   2.8     |   12
9.1.11      |   2.8     |   12        |   2.8  /  11 / 2.7+11 
    >> flexlibs 1.1.5:  Includes 2.7 & 11
9.1.15      |   2.9     |   13        |   2.9  /  13 / 2.8+13
    >> flexlibs 1.1.6:  Includes 2.7+2.8+2.9; & 11+12+13
