flexlibs
========

flexlibs is a library for accessing FieldWorks Language Explorer 
(FLEx) [1]_ projects.

flexlibs handles the necessary initialisation of the FLEx engine, and 
provides a class (FLExProject) for opening a FLEx project and working 
with its contents.

For the GUI application that runs Python scripts/plugins
on FLEx databases see FLExTools [2]_, which is built on flexlibs.


Requirements
------------
flexlibs supports Python 3.6, 3.7 and 3.8.

Python for .NET [3]_ version 2.5.

FieldWorks Language Explorer 9.0.17 Stable Release or higher.


32-bit vs 64-bit
^^^^^^^^^^^^^^^^
The Python architecture must match that of FieldWorks. I.e. Install 
32-bit Python for 32-bit Fieldworks, and 64-bit Python for 64-bit 
Fieldworks.

Installation
------------
Run:
``pip install flexlibs``

--------------

.. [1] https://software.sil.org/fieldworks/
.. [2] https://github.com/cdfarrow/flextools/wiki/
.. [3] https://github.com/pythonnet/pythonnet
