#coding:UTF-8
import time
from RfSwitch3499 import *

rfswitch = Rf3499()
time.sleep(2)
rfswitch.ToPipe('4')
time.sleep(2)
a = rfswitch.checkStatus()
print "haha",a
