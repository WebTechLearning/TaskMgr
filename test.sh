#/bin/tcsh

set py3=/home/klyuan/local/Python-3.5.1/bin/python3

$py3 taskMgr.py new AP-1 'AP #1'
$py3 taskMgr.py new AP-2 'AP #2'
$py3 taskMgr.py new AP-3 'AP #3'
$py3 taskMgr.py remove AP-3 
$py3 taskMgr.py move AP-1 -to today
$py3 taskMgr.py move AP-2 -to week
$py3 taskMgr.py show 
