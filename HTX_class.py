################################################################################
# @version               v1
# @date                  2014-08-10
# @author                Yunpeng
# @draft                 Roger Zhang
# 
# @Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import sys
import os
import time
import datetime
import telnetlib
import string
import re
import xml.dom.minidom
from comtypes.client import CreateObject

ETM1_1  202590
def makeConfig_singelCar(unitModel,TMmode,carrierbandwidth,):
    config = ('<SetItUpRequest><Unit><CommonName>%s</CommonName><UnitInChainId>0</UnitInChainId><Pipe id="0" nominalPower="36.99"><Carrier id="0"><Antenna id="0" testModelName="%s" nominalPower="36.99" scale="0" bw="%s" mimoId="-1" cellId="1" ></Antenna></Carrier></Pipe><Pipe id="1" nominalPower="36.99"><Carrier id="0"><Antenna id="0" testModelName="%s" nominalPower="36.99" scale="0" bw="%s" mimoId="-1" cellId="1" ></Antenna></Carrier></Pipe><RadioSpecific><GSM><DlControlPayloadOffset>0</DlControlPayloadOffset><ExtraNumberOfSlotsToCapture>1</ExtraNumberOfSlotsToCapture></GSM></RadioSpecific></Unit><Connections><SM2Unit><DeltaCorrection>%s</DeltaCorrection><SM_MasterPort><IP>192.168.255.16</IP></SM_MasterPort><SlavePort><UnitInChainId>0</UnitInChainId><Id>0</Id><UnitIP>192.168.255.69</UnitIP><FilterIP>192.168.255.70</FilterIP></SlavePort></SM2Unit></Connections></SetItUpRequest>' % unitModel,)
    return config

FHGA_BW5_config = '<SetItUpRequest><Unit><CommonName>FHGA</CommonName><UnitInChainId>0</UnitInChainId><Pipe id="0" nominalPower="36.99"><Carrier id="0"><Antenna id="0" testModelName="ETM1_1" nominalPower="36.99" scale="0" bw="5" mimoId="-1" cellId="1" ></Antenna></Carrier></Pipe><Pipe id="1" nominalPower="36.99"><Carrier id="0"><Antenna id="0" testModelName="ETM1_1" nominalPower="36.99" scale="0" bw="5" mimoId="-1" cellId="1" ></Antenna></Carrier></Pipe><RadioSpecific><GSM><DlControlPayloadOffset>0</DlControlPayloadOffset><ExtraNumberOfSlotsToCapture>1</ExtraNumberOfSlotsToCapture></GSM></RadioSpecific></Unit><Connections><SM2Unit><DeltaCorrection>202590</DeltaCorrection><SM_MasterPort><IP>192.168.255.16</IP></SM_MasterPort><SlavePort><UnitInChainId>0</UnitInChainId><Id>0</Id><UnitIP>192.168.255.69</UnitIP><FilterIP>192.168.255.70</FilterIP></SlavePort></SM2Unit></Connections></SetItUpRequest>'

EARFCN = {            #every row stand for Fdl_low,Noffs-DL,Ful_low,Noffs-UL
        1:[2110,0,1920,18000],
        2:[1930,600,1850,18600],
        3:[1805,1200,1710,19200],
        4:[2110,1950,1710,19950],
        5:[869,2400,824,20400],
        6:[875,2650,830,20650],
        7:[2620,2750,2500,20750],
        8:[925,3450,880,21450],
        9:[1844.9,3800,1749.9,21800],
        10:[2110,4150,1710,22150],
        11:[1475.9,4750,1427.9,22750],
        12:[729,5010,699,23010],
        13:[746,5180,777,23180],
        14:[758,5280,788,23280],
        17:[734,5730,704,23730],
        18:[860,5850,815,23850],
        19:[875,6000,830,24000],
        20:[791,6150,832,24150],
        21:[1495.9,6450,1447.9,24450],
        22:[3510,6600,3410,24600],
        23:[2180,7500,2000,25500],
        24:[1525,7700,1626.5,25700],
        25:[1930,8040,1850,26040],
        26:[859,8690,814,26690],
        27:[852,9040,807,27040],
        28:[758,9210,703,27210]
        }

class HTX(object):
    'remotecontrol HTX to set carrier and calc rxEvm'
    global engine
    engine =  win32com.client.Dispatch("HTX.Wrapper")
    
    def setUpHtx(uutname = "FHGA"):
        'select UUT'
        engine.setUnitTypeByName(uutname)
        
    def takedown(htx):
        returnStatus = HTX.takeDown()
        return returnStatus
    
    def setItUp(htx,carrierConfig):
        'sync htx with unit'
        returnStatus = htx.setUpConfiguration(FHGA_BW5_config)
        return returnStatus
    
    def RxOn(htx,pipe=0,antenna=0,carrier=0,ULchannel,DLchannel)
        htx.switchToUnitInChain(0)
        returnStatus = htx.rxOn(pipe,antenna,carrier,ULchannel,DLchannel)
        return returnStatus
        
    def RxOff(htx,pipe=0,antenna=0,carrier=0)
        htx.switchToUnitInChain(0)
        htx.rxOff(pipe,antenna,carrier)
    
    def TxOn(htx,pipe=0,antenna=0,carrier=0,ULchannel,DLchannel,rampit=1)
        htx.switchToUnitInChain(0)
        returnStatus = htx.txOn(pipe,antenna,carrier,ULchannel,DLchannel,rampit)
        return returnStatus
     
    def TxOff(htx,pipe=0,antenna=0,carrier=0,rampit=1)
        htx.switchToUnitInChain(0)
        htx.txOff(pipe,antenna,carrier,rampit)
    
    def activateCarrier(htx,pipe=0,carrier=0,ULchannel,DLchannel,rampit=1):
        returnStatus = htx.activateCarrier(pipe,carrier,ULchannel,DLchannel,rampit)
        return returnStatus
	
    def deactivateCarrier(htx):
        returnStatus = htx.deactivateCarrier(0,0,-1)
        return returnStatus
        
    def calcRxEvm(htx,freq,carrierband,testtimes,mudulation="QPSK",testgap='3'):
        iq = htx.captureIqData(1, -1)
        try:
            sqa = win32com.client.Dispatch("Sqa.Dsp")
        except:
            print "Dispatch SQA.dsp wrapper error!"
            sys.exit(0)
        if mudulation = "QPSK":
            sqa.setModulationQPSK()
        if mudulation = "16QAM":
            sqa.setModulation16QAM()
        rxevmRusults = build_Matrix(int(testtimes)+1,6)
        rxevmRusults[0] = ["RxEvm","carrierWidth(Mhz)","freq(Mhz)","RxEvm_max(%)","RxEvm_average(%)","RxEvm_alignment"]
        for i in range(1,int(testtimes)+1):   
            iq = htx.captureIqData(1, -1)
            temp = sqa.calculateEvmAsVariants(iq,5, 0 , 1 , 1, 0)
            rxevmRusults[i][1] = carrierband
            rxevmRusults[i][2] = freq
            data = temp.split(',')
            
            for j in range(3):
                aclrRusults[i][j+3] = data[j]
            time.sleep(int(testgap))
        return rxevmRusults
        
def freqtoChannel(txfreq,txband,rxfreq,rxband):
    'trun freq to channel number,PLS Attention:when the TX bands is not equal to RX bands,the tx and rx carrier maybe can not be active at the same time'
    channel=[0,0]  # first value is channel number of DL,second is channel number of UL
    Fdl_low = EARFCN[int(txband)][0]
    Noffs_dl = EARFCN[int(txband)][1]
    Ful_low = EARFCN[int(rxband)][2]
    Noffs_ul = EARFCN[int(rxband)][3]
    channel[0] = 10*(int(freq) - Fdl_low) + Noffs_dl
    channel[1] = 10*(int(freq) - Ful_low) + Noffs_ul
    return channel