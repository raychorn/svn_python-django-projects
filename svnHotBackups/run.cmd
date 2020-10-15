@echo off
cls
echo BEGIN:

set PYTHONPATH=c:\python25\lib;Z:\python projects\@lib;

REM python svnHotBackups.py --archive-type=bzip --num-backups=100 --repo-path=Z:\svn --backup-dir=C:\@1d

REM python sftp.py --computer=misha-lap.ad.magma-da.com --verbose --server=river --username=sfscript --password=sf@magma05 --source=C:\@1d\*.zip --dest=/home/sfscript/@data

REM python sftp.py --computer=misha-lap.ad.magma-da.com --verbose --server=river --username=sfscript --password=sf@magma05 --source=C:\@1d\*.gz --dest=/home/sfscript/@data

REM python sftp.py --computer=misha-lap.ad.magma-da.com --verbose --server=river --username=sfscript --password=sf@magma05 --source=C:\@1d\*.txt --dest=/home/sfscript/@data

REM C:\@utils\svnHotBackups\bin\svnHotBackups.exe --restore="C:\#svn_backups\avikohn\avikohn-2.bzip" --repo-path="C:\#svn_backups\avikohn-restore" > run_log_avikohn.txt

REM --verbose --archive-type=bzip --num-backups=4 --repo-path="F:\#svn\repo1" --backup-dir="F:/#svn_backups/repo1" --carbonite="P:\#svn_backups" --carbonite-hours=24 --carbonite-files=4 --carbonite-optimize=1 --carbonite-schedule=?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*

echo END!
