@echo off

cd %~dp0\

rem python checking...
echo python checking...

setlocal

rem 尝试运行Python 3并检查其版本
python --version > nul 2>&1
if %errorlevel% equ 0 (
    echo Python 3 is installed and the version is:
    python --version
    goto venv_create
) else (
    echo Python 3 is not installed or not properly configured in the system PATH.
    echo Please install Python 3 and ensure it is added to the PATH.
    goto python_install
)

endlocal

:python_install
rem Install Python in silent mode
echo ----------------------------------
echo start to install Python, please wait......
python-3.6.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
if %errorlevel%==0 (echo Python3.6 install successfully! & goto venv_create) else (echo Python installation failed! & goto quit)

:venv_create
rem venv creating...
echo venv creating...
rem 创建虚拟环境
echo "start check requirements.txt file"
if exist %~dp0\requirements.txt (
   echo "check requirements.txt finish"
) else (
  echo "not exist requirements.txt" & goto quit
)
echo "start init env"
SET curdir=%~dp0\venv
echo %curdir%
if exist  %curdir% (
 rem RD /S /q %~dp0\venv
 rem echo "delete old  venv"
 rem TIMEOUT /T 8
 rem echo "start create new venv"
 rem python -m venv ./venv
 rem TIMEOUT /T 5
 echo "create new venv finish"
) else (
 python -m venv ./venv
 echo "finish create venv"
)

rem pip updating...
echo pip updating...
call %~dp0\venv\Scripts\activate.bat venv
pip list
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install --upgrade pip
pip list

rem requirements downloading...
echo requirements downloading...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
if %errorlevel% equ 0 (
    echo Python 3 is installed and the version is:
) else (
    echo Requirements downloading unsuccessful! Please follow the tips.txt and restart this file later...
    start "" "Tips.txt"
    goto quit
)

rem start...
echo start...
python %~dp0\Main.py

:quit
set /p tmp=All successfully done. Press any key to exit...
