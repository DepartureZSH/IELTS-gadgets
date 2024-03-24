@echo off

rem 创建虚拟环境
echo "start check requirements.txt file"
if exist %cd%\requirements.txt (
   echo "check requirements.txt finish"
) else (
  echo "not exist requirements.txt"
)   
echo "start init env"
SET curdir=%cd%\venv
echo %curdir%
if exist  %curdir% (
 RD /S /q %cd%\venv
 echo "delete old  venv"
 TIMEOUT /T 8
 echo "start create new venv"
 python -m venv ./venv
 TIMEOUT /T 5
 echo "create new venv finish"
) else (
 python -m venv ./venv
 echo "finish create venv"
)
call init_venv.bat