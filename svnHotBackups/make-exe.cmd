@echo off

cls
echo BEGIN:

if exist "Z:\python projects\@lib" set PYTHONPATH=c:\python25\lib;Z:\python projects\@lib;
if exist "F:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python25\lib;F:\@Vyper Logix Corp\@Projects\python\@lib;
if exist "J:\@Vyper Logix Corp\@Projects\python\@lib" set PYTHONPATH=c:\python25\lib;J:\@Vyper Logix Corp\@Projects\python\@lib;

if 0%1. == 0. goto help

if exist stdout*.txt del stdout*.txt

if %1. == 1. python25 -O setup_svnHotBackups.py py2exe --packages=Crypto,paramiko
if %1. == 2. python25 -O setup_sftp.py py2exe --packages=Crypto,paramiko

goto end

:help
echo Begin: ---------------------------------------------------------------------------------------------------
echo "1" means setup_svnHotBackups.py
echo "2" means setup_sftp.py
echo END! -----------------------------------------------------------------------------------------------------

:end

echo END!

