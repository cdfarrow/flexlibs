Background:

From time to time Fieldworks updates the version of third-party dlls 
that it includes in its installation, even though not all Fieldworks 
libraries are updated to use the new version. This discrepancy is 
handled with a (version) redirection in the Fieldworks.exe.config 
file. Other applications, such as Phonology Assistant include the 
later versions, and also use redirection in the .config file.

Because FlexTools is a python application, we can't easily use a 
.config file. We would have to either include python (with its exe) in 
the distribution, or create a simple wrapper exe that calls python.

The alternative is to include the old dlls in the FlexTools 
installation, which is the current solution being used. If/when it 
comes up again, simply add the *old* dll into this folder.

----------------------------------------------------------- 

History:

Fieldworks 9.0.8 installs v12 of Newtonsoft.JSON.dll.
--> v11 from FW 9.0.7 is included here.

Fieldworks 9.1.9 installs v2.8 of icu.net.dll
--> v2.7 from FW 9.1.8 is included here along with 
Microsoft.Extensions.DependencyModel.dll, which is referenced 
by icu.net.dll.
