@ECHO OFF
REM Simple build commands for flexlibs

REM Build with the default Python version
set PYTHON=py

REM Check that the argument is a valid command, and do it. /I ignores case.
FOR %%C IN ("Init"
            "Test"
            "Clean"
            "Build"
            "Publish") DO (
            IF /I "%1"=="%%~C" GOTO :Do%1
)
    
:Usage
    echo Usage:
    echo      make init         - Install the libraries for building
    echo      make test         - Run the unit tests
    echo      make clean        - Clean out build files
    echo      make build        - Build the project
    echo      make publish      - Publish the project to PyPI
    goto :End

:DoInit
    %PYTHON% -m pip install -r requirements.txt
    goto :End
    
:DoTest
    %PYTHON% -m pytest
    goto :End

:DoClean
    rmdir /s /q ".\build"
    rmdir /s /q ".\dist"
    rmdir /s /q ".\flexlibs\docs"
    goto :End
    
:DoBuild
    @REM Build the Sphinx docs
    sphinx-build docs/sphinx flexlibs/docs/flexlibsAPI

    @REM Build the wheel with setuptools
    %PYTHON% -m build -w -nx
    
    @REM Check for package errors
    %PYTHON% -m twine check .\dist\*
    goto :End
    
:DoPublish
    echo Publishing wheel to PyPI
    %PYTHON% -m twine upload .\dist\flexlibs*
    goto :End


:End
