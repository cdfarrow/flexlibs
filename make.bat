@ECHO OFF
REM Simple build commands for flexlibs

REM We require this version of Python for doing the build
set PYTHON=py -3.8

REM Check that the argument is a valid command, and do it. /I ignores case.
FOR %%C IN ("Init"
            "Clean"
            "Build"
            "Publish") DO (
            IF /I "%1"=="%%~C" GOTO :Do%1
)
    
:Usage
    echo Usage:
    echo      make init
    echo      make clean
    echo      make build
    echo      make publish
    exit

:DoInit
    %PYTHON% -m pip install -r requirements.txt
    exit
    
:DoClean
    rmdir /s /q ".\build"
    rmdir /s /q ".\dist"
    rmdir /s /q ".\flexlibs\docs"
    exit
    
:DoBuild
    @REM Build the Sphinx docs
    sphinx-build docs/sphinx flexlibs/docs/flexlibsAPI

    @REM Build the Wheel
    %PYTHON% -m build -w
    exit
    
:DoPublish
    echo Not implemented yet :-)
    exit
