@echo on

set PYTHONPATH=c:\python27;

if exist compile-all.pyc del compile-all.pyc
if exist compile-all.pyo del compile-all.pyo

if exist "J:\@Vyper Logix Corp\@Projects\python\@lib\dist_2.7.0" rmdir /S /Q "J:\@Vyper Logix Corp\@Projects\python\@lib\dist_2.7.0"

c:\python27\python2.7.exe -OO compile-all.py > compile2.7.log 2>&1
