#coding:UTF-8

#*****************************************************************************
#* File:    class_FSV.py
#* Author:  Yunpeng
#* Date:    27-04-2016
#* This script controls FSV of R&S.
#* 
#*****************************************************************************

import telnetlib
import time
#import platform
#import subprocess
import sys
import os
#import visa


class FSV_telnet(object):
    IPaddress = ""
    unit_username = ""
    unit_password = ""
    prompt = "rfsw> "
    client = None
    channel = None
    verbose = 7
    TheEquipment = None
    
    freq = "877.5"     # unit in MHz,support 2~6Ghz
    band = "5"       # unit in MHz,support 1.4\3\5\10\15\20 Mhz(in LTE mode)
    cableloss = "67" # unit in db
    times = "3"     # test times(if test n times,will get n group of value in log file)
    gap = "3"      #unit in second,the wait time between two test
    

    def __init__(self,IPaddress):
        print "seting new FSV"
        self.TheEquipment = telnetlib.Telnet(IPaddress, port=5025)
        self.TheEquipment.write("*IDN?" + "\n")
        time.sleep(1)
        a = self.TheEquipment.read_very_eager()
        print a
        
    def gotoLtemode(self,frequency,bandwidth,cableloss):
        dict_SupportBands = {'1.4':'1_40', '3':'3_00', '5':'5_00','10':'10_00','15':'15_00','20':'20_00'}
        s_BW = dict_SupportBands[bandwidth]
        cmds1 = ["*RST","INIT:CONT OFF","SYST:DISP:UPD ON","INST LTE","FREQ:CENT "+frequency+"MHz","CONF:DL:BW BW"+s_BW,"POW:AUTO2 ON","DISP:TRAC:Y:RLEV:OFFS "+cableloss]
        for i in range(0,len(cmds1)):
            self.TheEquipment.write(cmds1[i] + "\n")
            time.sleep(2)
            #print("==> SEND : %s " % cmds1[i])
        print "LTE mode set done!"
        
    def prepareACLR(self):
        cmds1 = ["CALC2:FEED 'SPEC:ACP'","INIT:CONT OFF"]
        for i in range(0,len(cmds1)):
            self.TheEquipment.write(cmds1[i] + "\n")
            time.sleep(2)
            #print("==> SEND : %s " % cmds1[i])
        print "Aclr prepare done!"
    
    def testACLR(self):
        print("query ACLR result")
        self.TheEquipment.write("INIT;*WAI\n") # execute test for one time
        time.sleep(2)
        self.TheEquipment.write("CALC1:MARK:FUNC:POW:RES?\n") # ask for aclr result
        time.sleep(1)
        a = self.TheEquipment.read_very_eager()
        print "Get ACLR result!"
        return a
    
    def prepareTxEvm(self):
        cmds1 = ["CALC2:FEED 'STAT:ASUM'","INIT:CONT OFF"]
        for i in range(0,len(cmds1)):
            self.TheEquipment.write(cmds1[i] + "\n")
            time.sleep(2)
            #print("==> SEND : %s " % cmds1[i])
        print "TX-EVM prepare done!"
        
    def testTxEvm(self):
        print "query TxEvm result"
        self.TheEquipment.write("INIT;*WAI\n") # execute test for one time
        time.sleep(2)
        self.TheEquipment.write("FETC:SUMM:EVM?"+"\n") # ask for EVM result
        time.sleep(1)
        a1 = self.TheEquipment.read_very_eager()
        return a1
'''
# manually setting the ESG and save the file to the ESG, the command will be
#*SAV 7
#then we need to store the file to the right location
:MMEMory:STOR:STATe 7,"d:\7.savcrl"
# Then we can recall all the file we need
*RCL 7
'''
        
