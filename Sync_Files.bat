@ECHO OFF
cd "F:\Work Files\Python Scripts\Sync Work Files"
set p1=-hostdir="F:\Work Files"
set p2=-destdir="C:\Users\matth\Desktop\Files\Back-Ups\Work Materials"
python -u Sync_Work_Files.py -syncall %p1% %p2%
pause