:: Script: `.\Wsl2-AmdGpu-Chat.Bat`

:: Initialization
@echo off
setlocal enabledelayedexpansion
title Wsl2-AmdGpu-Chat
color 80
echo Initialization Complete.
timeout /t 1 >nul

:: Globals Block - Customize here if needed
set "PYTHON_EXE_TO_USE=python3"
set "REQUIREMENTS_LIST=transformers--4.37.0 ctransformers--latest torch-directml--latest"
set "PERSISTENCE_FILE=./data/persistence.txt"
set "WSL_DISTRIBUTION="
set "CLBLAS_INSTALLED="

:: DP0 TO SCRIPT BLOCK, DO NOT, MODIFY or MOVE: START
set "ScriptDirectory=%~dp0"
set "ScriptDirectory=%ScriptDirectory:~0,-1%"
cd /d "%ScriptDirectory%"
echo Dp0'd to Script.
:: DP0 TO SCRIPT BLOCK, DO NOT, MODIFY or MOVE: END

:: Ensure the ./data directory and persistence.txt file exist
if not exist .\data (
    echo Creating ./data directory...
    mkdir .\data
)
if not exist %PERSISTENCE_FILE% (
    echo No persistence file found.
    echo Listing WSL distributions...
    wsl -l
    echo.
    set /p WSL_DISTRIBUTION=Please enter the name of your WSL distribution: 
    
    :: Validate the entered WSL distribution
    for /f "tokens=*" %%i in ('wsl -l') do (
        if /i "%%i"=="%WSL_DISTRIBUTION%" (
            echo Saving distribution name to persistence.txt...
            echo %WSL_DISTRIBUTION% > %PERSISTENCE_FILE%
            goto :continue_script
        )
    )
    echo Error: Invalid WSL distribution entered.
    pause
    goto :main_menu
) else (
    echo Reading WSL distribution from persistence.txt...
    set /p WSL_DISTRIBUTION=<%PERSISTENCE_FILE%
    echo Using distribution: %WSL_DISTRIBUTION%
)

:: Check if ClBlas is installed and update the variable
for /f "tokens=*" %%i in (%PERSISTENCE_FILE%) do (
    if "%%i"=="clblas_installed=true" (
        set CLBLAS_INSTALLED=true
    )
)

:continue_script

:: Banner Function
:main_banner
cls
echo ========================================================================================================================
echo     Wsl2-AmdGpu-Chat
echo ========================================================================================================================
echo.
goto :eof

:: Main Code Begin
:main_menu
call :main_banner
echo     1. Run Wsl2-AmdGpu-Chat
echo.
echo     2. Install Python Requirements
echo.
echo     3. Install Github Requirements
echo.
echo ========================================================================================================================
set /p choice=Selection; Menu Options = 1-3, Exit = X: 

if /i "!choice!"=="1" (
    echo Selected: Run Chatbot
    timeout /t 1 >nul
    goto run_chatbot
) else if /i "!choice!"=="2" (
    echo Selected: Install Requirements
    timeout /t 1 >nul
    goto run_setup_install
) else if /i "!choice!"=="3" (
    echo Selected: Install ClBlas
    timeout /t 1 >nul
    goto install_clblas
) else if /i "!choice!"=="X" (
    echo Exiting...
    timeout /t 1 >nul
    goto :end_of_file
) else (
    echo Invalid option. Please try again.
    pause
    goto :main_menu
)

:: Run Chatbot
:run_chatbot
call :main_banner
echo Launching Chatbot in WSL2 environment...

:: Use WSL to run the Python script inside the Linux environment
wsl -d %WSL_DISTRIBUTION% %PYTHON_EXE_TO_USE% ./wsl2_amdgpu_chat.py

echo.
pause
goto main_menu

:: Install Python Requirements in WSL2
:run_setup_install
call :main_banner
echo Installing required Python packages...

:: Upgrading pip in WSL
wsl -d %WSL_DISTRIBUTION% %PYTHON_EXE_TO_USE% -m pip install --upgrade pip
echo Pip Upgraded.
echo.

:: Install each package by converting "--" to "=="
set "errorPackages="  :: Initialize error packages list
for %%p in (%REQUIREMENTS_LIST%) do (
    set "package=%%p"
    set "package=!package:--==!"
    echo Installing !package!...
    wsl -d %WSL_DISTRIBUTION% %PYTHON_EXE_TO_USE% -m pip install !package!
    if errorlevel 1 (
        echo Failed to install !package!. Adding to error list...
        set "errorPackages=!errorPackages! !package!"
    ) else (
        echo !package! installed successfully.
    )
    echo.
)

:: Check for package installation issues
echo Verifying Packages...
if not "!errorPackages!"=="" (
    echo Error packages found: !errorPackages!
) else (
    echo Requirements Installed Successfully.
)

echo.
pause
goto main_menu

:: Install CLBlast
:install_clblas
call :main_banner
echo Installing CLBlast...

:: Install necessary dependencies and clone CLBlast
wsl -d %WSL_DISTRIBUTION% sudo apt-get install git cmake make -y
wsl -d %WSL_DISTRIBUTION% git clone https://github.com/CNugteren/CLBlast.git

:: Build and install CLBlast
wsl -d %WSL_DISTRIBUTION% bash -c "cd CLBlast && mkdir build && cd build && cmake .. && make && sudo make install"

:: Update persistence to track that CLBlast is installed
echo clblas_installed=clblast >> %PERSISTENCE_FILE%

echo CLBlast installed successfully.
pause
goto main_menu

:: Invalid input, re-prompt user
echo Invalid selection. Please choose either 1 or 2.
pause
goto install_clblas


:end_of_file
call :main_banner
echo Exiting...
timeout /t 1 >nul
exit /b