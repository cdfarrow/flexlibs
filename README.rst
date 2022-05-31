flexlibs
========

flexlibs is a library for accessing FieldWorks Language Explorer 
(FLEx) [1]_ projects.

flexlibs handles the necessary initialisation of the FLEx engine, and 
provides a class (FLExProject) for opening a FLEx project and working 
with its contents.

`FLExTools <https://github.com/cdfarrow/flextools/wiki/>` is an 
application for running Python scripts on FLEx databases. It is built 
on flexlibs.


Requirements
------------
flexlibs supports Python 2.7, 3.5, 3.6, 3.7 and 3.8.

Python for .NET [2]_ version 2.0.0 or greater.

FieldWorks Language Explorer 9.0.4 beta or higher.

Python 2.7 requires the future package (``pip install future``)

32-bit vs 64-bit
^^^^^^^^^^^^^^^^
The Python architecture must match that of FieldWorks. I.e. Install 
32-bit Python for 32-bit Fieldworks, and 64-bit Python for 64-bit 
Fieldworks.

Installation
------------
Run:
pip install git+https://github.com/cdfarrow/flexlibs

--------------

.. [1] https://software.sil.org/fieldworks/
.. [2] https://github.com/pythonnet/pythonnet
