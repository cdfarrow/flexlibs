@ECHO OFF
REM Simple build commands for flexlibs
SETLOCAL EnableExtensions EnableDelayedExpansion

REM Prefer a supported Python (flexlibs requires >=3.8,<3.14).
REM Override with: set PYTHON=py -3.11
if not defined PYTHON (
    call :FindPython
    if not defined PYTHON (
        echo No supported Python found ^(need 3.8-3.13^). Install one or set PYTHON=.
        exit /b 1
    )
)
echo Using PYTHON=%PYTHON%

REM Check that the argument is a valid command, and do it. /I ignores case.
FOR %%C IN ("Init"
            "Test"
            "Test-nuget"
            "Clean"
            "Build"
            "Publish") DO (
            IF /I "%1"=="%%~C" GOTO :Do%1
)
    
:Usage
    echo Usage:
    echo      make init         - Install the libraries for building
    echo      make test         - Run the unit tests
    echo      make test-nuget   - Restore latest SIL NuGet packages and run tests with overlay
    echo      make clean        - Clean out build files
    echo      make build        - Build the project
    echo      make publish      - Publish the project to PyPI
    echo.
    echo Extra args after test / test-nuget are passed to pytest, e.g.:
    echo      .\make.bat test-nuget -k "not CustomFields" -q
    exit /b 1

:DoInit
    %PYTHON% -m pip install -r requirements.txt
    exit /b !ERRORLEVEL!
    
:DoTest
    call :CollectPytestArgs %*
    %PYTHON% -m pytest !PYTEST_ARGS!
    exit /b !ERRORLEVEL!

:DoTest-nuget
    call :CollectPytestArgs %*
    powershell -NoProfile -ExecutionPolicy Bypass -File ".\tests\nuget-overlay\restore.ps1"
    if errorlevel 1 exit /b 1
    set "FLEXLIBS_ASSEMBLY_DIR=%CD%\.fw-nuget-overlay"
    %PYTHON% -m pytest !PYTEST_ARGS!
    exit /b !ERRORLEVEL!

:DoClean
    if exist ".\build" rmdir /s /q ".\build"
    if exist ".\dist" rmdir /s /q ".\dist"
    if exist ".\flexlibs\docs" rmdir /s /q ".\flexlibs\docs"
    if exist ".\.fw-nuget-overlay" rmdir /s /q ".\.fw-nuget-overlay"
    if exist ".\tests\nuget-overlay\bin" rmdir /s /q ".\tests\nuget-overlay\bin"
    if exist ".\tests\nuget-overlay\obj" rmdir /s /q ".\tests\nuget-overlay\obj"
    exit /b 0
    
:DoBuild
    @REM Build the Sphinx docs
    sphinx-build docs/sphinx flexlibs/docs/flexlibsAPI
    if errorlevel 1 exit /b 1

    @REM Build the wheel with setuptools
    %PYTHON% -m build -w -nx
    if errorlevel 1 exit /b 1
    
    @REM Check for package errors
    %PYTHON% -m twine check .\dist\*
    exit /b !ERRORLEVEL!
    
:DoPublish
    echo Publishing wheel to PyPI
    %PYTHON% -m twine upload .\dist\flexlibs*
    exit /b !ERRORLEVEL!

:FindPython
    for %%V in (3.13 3.12 3.11 3.10 3.9 3.8) do (
        py -%%V -c "import sys" >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            set "PYTHON=py -%%V"
            goto :eof
        )
    )
    goto :eof

:CollectPytestArgs
    REM Drop the make command (%1), keep the rest for pytest.
    set "PYTEST_ARGS="
    shift
:CollectPytestArgsLoop
    if "%~1"=="" goto :eof
    set "PYTEST_ARGS=!PYTEST_ARGS! %1"
    shift
    goto CollectPytestArgsLoop
