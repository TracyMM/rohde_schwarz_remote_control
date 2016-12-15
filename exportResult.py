#!/usr/bin/python
# coding: utf-8

import xlwt
import sys
import time
import xlrd
from xlutils.copy import copy

def setstyle(fontsize,backcolor,bold=False,):
    style = xlwt.XFStyle() 
 
    font = xlwt.Font()   #set font
    font.name = 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = fontsize
 
    borders= xlwt.Borders()   #set border
    borders.left= 1
    borders.right= 1
    borders.top= 1
    borders.bottom= 1
  
    pattern = xlwt.Pattern() # set Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = backcolor # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
  
  
    style.font = font
    style.borders = borders
    style.pattern = pattern
    return style


def createEmptyXls(xlsName,sheetName):
    bookname = xlsName+'.xls'
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetName)
    wb.save(bookname)
    
def addData2Xls(Data,emptyXlsName,beginRow):
    carrierband = N[1][1]
    xlsname = emptyXlsName+".xls"
    yvalue = beginRow-1
    print yvalue
    doubleband = str(2*int(carrierband))
    
    oldWorkbook = xlrd.open_workbook(xlsname, formatting_info=True)
    newWorkbook = copy(oldWorkbook)
    newWS = newWorkbook.get_sheet(0)
    
    #print header
    newWS.row(yvalue).height = 1500
    newWS.col(0).width = 3333
    newWS.col(1).width = 3333
    newWS.col(2).width = 3333
    for i in range(3,len(Data[0])):
        newWS.col(i).width= 4000
    
    newWS.write(yvalue,0,Data[0][0],setstyle(230,3,True))     #write mark
    for i in range(1,len(Data[0])):                          #write header line
        newWS.write(yvalue,i,Data[0][i],setstyle(200,22,True))
    for i in range(len(Data)-1):                                          #write data
        for j in range(len(Data[0])-1):
            newWS.write(yvalue+1+i,j+1,Data[i+1][j+1],setstyle(180,1,False))
    newWorkbook.save(xlsname)

timestamp = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
sheetname = "testResult_"+timestamp          
xlsname = 'FHGA'+"_"+timestamp

createEmptyXls(xlsname,sheetname)
N=[['RxEvm','carrierBand','freq','Txevm-avg','Txevm-max','Txevm-min'],['','10','5','3.1','1.2','-3100'],['','10','5','2.9','1.1','-3300']]
print N
addData2Xls(N,xlsname,1)    

M=[['RxEvm','carrierBand','freq','Txevm-avg','Txevm-max','Txevm-min'],['','10','5','3.1','1.2','-3100'],['','10','5','2.9','1.1','-3300']]
addData2Xls(N,xlsname,1+len(N)+2)