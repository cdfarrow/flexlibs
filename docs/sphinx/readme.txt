The Sphinx configuration was created by:

    1. sphinx-apidoc -o <outputdir> <package-dir>
       i.e. sphinx-apidoc -o sphinx flexlibs

    2. Editing the conf.py file to specify version, author, etc.
       Editing flexlibs.rst to include only the FLExProject class

The documentation is built with:
    sphinx-build -b html docs/sphinx flexlibs/docs/flexlibsAPI
    (This is what make.bat does)
