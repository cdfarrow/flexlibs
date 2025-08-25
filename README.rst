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

Python 3.8 - 3.13.

Python for .NET [3]_ version 3.0.3+.

FieldWorks Language Explorer 9.0.17 - 9.3.1.


32-bit vs 64-bit
^^^^^^^^^^^^^^^^
The Python architecture must match that of FieldWorks. I.e. Install 
32-bit Python for 32-bit Fieldworks, and 64-bit Python for 64-bit 
Fieldworks.

Installation
------------
Run:
``pip install flexlibs``

Usage
-----

.. code-block:: python


  import flexlibs
  flexlibs.FLExInitialize()
  p = flexlibs.FLExProject()
  p.OpenProject('parser-experiments')
  p.GetPartsOfSpeech()
  # ['Adverb', 'Noun', 'Pro-form', 'Pronoun', 'Verb', 'Copulative verb', 'Ditransitive verb', 'Intransitive verb', 'Transitive verb', 'Coordinating connective']

  # The API documentation is an HTML file
  os.startfile(flexlibs.APIHelpFile)
  ...
  p.CloseProject()
  flexlibs.FLExCleanup()

--------------

.. [1] https://software.sil.org/fieldworks/
.. [2] https://github.com/cdfarrow/flextools/wiki/
.. [3] https://github.com/pythonnet/pythonnet/wiki
