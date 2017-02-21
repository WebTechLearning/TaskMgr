#!/home/klyuan/local/Python-3.5.1/bin/python3
import os

os.system('/home/klyuan/local/Python-3.5.1/bin/python3 taskMgr.py new AP-1 \'AP No.1\'') 
os.system('/home/klyuan/local/Python-3.5.1/bin/python3 taskMgr.py new AP-2 \'AP No.2\'') 
os.system('/home/klyuan/local/Python-3.5.1/bin/python3 taskMgr.py new AP-3 \'AP No.3\'') 
os.system('/home/klyuan/local/Python-3.5.1/bin/python3 taskMgr.py remove AP-3') 
os.system('/home/klyuan/local/Python-3.5.1/bin/python3 taskMgr.py move AP-1 -to today') 
os.system('/home/klyuan/local/Python-3.5.1/bin/python3 taskMgr.py move AP-2 -to week') 
os.system('/home/klyuan/local/Python-3.5.1/bin/python3 taskMgr.py show') 
