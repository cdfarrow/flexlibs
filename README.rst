flexlibs
========

flexlibs is a library for accessing FieldWorks Language Explorer (FLEx) [1]_ projects.

flexlibs handles the necessary initialisation of the FLEx engine, and 
provides a class (FLExProject) for opening a FLEx project and working 
with its contents.


Requirements
------------
flexlibs is supported for Python 2.7, 3.5, 3.6, and 3.7.

Python for .NET [2]_ version 2.0.0 or greater is required. For Python 3.7, pythonnet must currently be checked out and compiled
from source (master branch).

FieldWorks Language Explorer 9.0.4 beta or higher must be installed on the system.

32-bit vs 64-bit FieldWorks
^^^^^^^^^^^^^^^^^^^^^^^^^^^
32-bit FieldWorks requires the use of 32-bit Python.

64-bit FieldWorks requires the use of 64-bit Python.


--------------

.. [1] https://software.sil.org/fieldworks/
.. [2] https://github.com/pythonnet/pythonnet
