
#! /usr/bin/env python
#*****************************************************************************
#* File:    RfSwitch3499.py
#* Author:  Yunpeng Bai
#* Date:    01-Apr-2016
#* This script controls 3499 RFswitch.
#* 
#*****************************************************************************

#from instruments_v2 import *
import time
#import platform
#import subprocess
#import sys
#import os
import visa

class Rf3499(object):
    GPIBaddress = ""
    TheEquipment=None
    
    def __init__(self,GPIBaddress = "9"):
        print "access to 3499"
        rm = visa.ResourceManager()
        rm.list_resources()
        self.TheEquipment=rm.open_resource('GPIB0::'+GPIBaddress+'::INSTR')
        print self.TheEquipment.query("*IDN?")  
        
    def ToPipe(self,num):
        if num == '1':
            self.TheEquipment.write("close (@100,101,102)")
            print "switch to Pipe1"
        elif num == '2':
            self.TheEquipment.write("open (@100);close (@101,102)\n")
            print "switch to Pipe2"
        elif num == '3':
            self.TheEquipment.write("open (@101);close (@102)")
            print "switch to Pipe3"
        elif num == '4':
            self.TheEquipment.write("open (@102)")
            print "switch to Pipe4"
        else:
            print 'nothing done,pipe-num input is not right!!'
        
    def checkStatus(self):
        out = ""
        stat1 = str(self.TheEquipment.query("ROUT:OPEN? (@100,101,102)"))
        print 'stat is :',stat1,
        #print type(stat1)
        if stat1 == "0,0,0\n":
            out = "pipe1"
        elif stat1 == "1,0,0\n":
            out = "pipe2"
        elif stat1 == "1,1,0\n" or stat1 == "0,1,0\n":
            out = "pipe3"
        elif stat1.split(',')[2] == "1\n":
            out = "pipe4"
        else:
            out = 'Undefined status:'+stat1
        return out