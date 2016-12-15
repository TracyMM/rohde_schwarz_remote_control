#coding:UTF-8
import time
from class_FSV import *

fsv = FSV_telnet("10.140.198.20")
time.sleep(3)
fsv.gotoLtemode("874.5","5","67")
time.sleep(3)

'''
fsv.prepareACLR()
time.sleep(3)
re = fsv.testACLR()
print re
'''

fsv.prepareTxEvm()
time.sleep(3)
re = fsv.testTxEvm()
print re