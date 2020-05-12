@ECHO OFF
cd "<location of script>"
set p1=-hostdir="<path to external drive directory>"
set p2=-destdir="<path to destination directory>"
python -u Sync_Work_Files.py -syncall %p1% %p2%
pause
