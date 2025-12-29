@echo off
setlocal

:: Define source directory and target directory
set PROGRAM_NAME=sync_to_zentao
set ENTRY_DIR=%~dp0..\main

:: Start packaging the program
echo Packaging %PROGRAM_NAME%.exe...
cd "%ENTRY_DIR%"
echo y | pyinstaller --onefile --noupx --clean --log-level INFO --noconfirm ^
--hidden-import=json --hidden-import=colorama --hidden-import=jira --hidden-import=translate --hidden-import=openpyxl ^
--add-data "libmirror/mstr.py;." ^
--add-data "libmirror/mconfig.py;." ^
--add-data "libmirror/mio.py;." ^
--add-data "libmirror/mlogger.py;." ^
--add-data "libmirror/mpath.py;." ^
--add-data "libmirror/mjira/const.py;mjira" ^
--add-data "libmirror/mjira/field.py;mjira" ^
--add-data "libmirror/mjira/issue.py;mjira" ^
--add-data "libmirror/mjira/http.py;mjira" ^
--add-data "libmirror/mjira/net_sony.py;mjira" ^
--add-data "libmirror/mzendao/*.py;mzendao" ^
%PROGRAM_NAME%.py
if %errorlevel% neq 0 (
    echo Packaging failed, please check pyinstaller configuration!
    pause
    exit /b 1
)


echo Operation Completed
pause