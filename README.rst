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

Testing against latest NuGet packages
-------------------------------------

By default flexlibs loads FieldWorks assemblies from an installed FieldWorks
9.x tree (discovered via the Windows registry).

For integration testing against newer SIL libraries from nuget.org, restore
an overlay and run the existing tests::

  make test-nuget

This publishes the latest prerelease ``SIL.LCModel``, ``SIL.Core``,
``SIL.WritingSystems`` (and related) packages into ``.fw-nuget-overlay`` and
sets ``FLEXLIBS_ASSEMBLY_DIR`` so those DLLs shadow the copies from the
FieldWorks install. App assemblies such as ``FwUtils`` still come from
FieldWorks.

Environment overrides (useful for CI without a Windows installer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``FLEXLIBS_FW_CODE_DIR`` — directory containing ``FieldWorks.exe`` and app DLLs
- ``FLEXLIBS_FW_PROJECTS_DIR`` — FieldWorks projects directory (required when
  ``FLEXLIBS_FW_CODE_DIR`` is set)
- ``FLEXLIBS_ASSEMBLY_DIR`` — optional folder of DLLs prepended on the assembly
  search path (set automatically by ``make test-nuget``)

When the code/projects env vars are set, registry discovery is skipped. You
still need a complete FieldWorks binary tree (install or unzipped build) plus
matching Python bitness; NuGet alone does not supply ``FwUtils`` /
``FieldWorks.exe``.

Requires the .NET SDK (for ``dotnet publish``) in addition to the normal
test prerequisites.

The custom-field write test needs a FieldWorks project with an entry-level
custom text field. Defaults are project ``__flexlibs_testing`` and field
``EntryFlags``; override with::

  set FLEXLIBS_TEST_PROJECT=MyProject
  set FLEXLIBS_TEST_CUSTOM_FIELD=MyCustomField

The other tests use any project already present in the projects directory.

Skip the custom-field test (or pass any pytest args)::

  .\make.bat test-nuget -k "not CustomFields"


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
