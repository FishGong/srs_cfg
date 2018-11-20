#-------------------------------------------------------------------------------
# Name:        srs_cfg.py
# Purpose:     auto generate cfg file
#
# Author:      jegong
#
# Created:     15/03/2017
# Copyright:   (c) jegong 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os
import xlrd
import shutil
import math
import string

import srs_wb
import srs_nb
reload(sys)
sys.setdefaultencoding('utf-8')

ver = '2.0'
print "\nWelcome to the srs cfg wizard " + ver
print "Usage: python.exe srs_cfg.py D:\bcem.xls D:\n"

#(1) parameter check
#command line argument: ul_auto_gen_testcase.xls
strCmdLine0 = sys.argv[0]#python script file name
strCmdLine1 = sys.argv[1]#case list file
strCmdLine2 = sys.argv[2]#case cfg output location
print "(1) Interpret command line argument: " + strCmdLine0 + " " + strCmdLine1 + " " + strCmdLine2


if os.path.exists(strCmdLine1):
    print "Case list found in file " + strCmdLine1

    caseListXlsAbs=strCmdLine1
elif os.path.exists(os.getcwd()+"\\"+strCmdLine1):
    print "Case list found in file " + os.getcwd()+"\\"+strCmdLine1

    caseListXlsAbs=os.getcwd()+"\\"+strCmdLine1
else:
    print strCmdLine1 + " not found"
    print os.getcwd()+"\\"+strCmdLine1 + " not found"
    exit
output_name = os.path.basename(strCmdLine1).split('.')[0]
caseDir = strCmdLine2 + '\\' + output_name + '\\'

if os.path.exists(caseDir):
    shutil.rmtree(caseDir)#remove this dir
os.makedirs(caseDir)

#(2) parse the excel file, generate case dictionary
print "(2) Parse the xls and construct the testcase dictionary"
#structure of labelInfo: [[label, head, tail, []], ....]
labelInfo=[]
labelLast=''
labelCur=''
head=0
tail=0
#structure of testcaseDict: {testname:{firstLabel:{secondLable:value}}, ....}
dictTestcaseSheet = {}
testcaseDict={}
testcaseName=''


#read the excel
wb=xlrd.open_workbook(caseListXlsAbs)
for s in wb.sheets():#loop all sheets
    labelInfo=[]
    testcaseDict={}
    for row in range(s.nrows):#from 0 to s.nrows-1
        values=[]
        for col in range(s.ncols):
            if row==0:
                #get the 1st level labels
                if s.cell(row,col).value != '':
                    labelCur = s.cell(row,col).value
                    if col == 0:
                        labelLast = labelCur
                        head = 0
                    tail = col-1
                    if tail != -1:
                        #not the first label in the first row
                        labelInfo.append([labelLast, head, tail, []])
                        labelLast = labelCur
                        head = col
                else:
                    if col == (s.ncols-1):
                        tail = col
                        labelInfo.append([labelCur, head, tail, []])
            elif row==1:
                #get the 2nd level labels
                for firstLevelIdx in range(len(labelInfo)):
                    if labelInfo[firstLevelIdx][1] <= col <= labelInfo[firstLevelIdx][2]:
                        if s.cell(row,col).value == '':
                            labelInfo[firstLevelIdx][3].append(labelInfo[firstLevelIdx][0])
                        else:
                            labelInfo[firstLevelIdx][3].append(s.cell(row,col).value)
                        break
            else:
                #Caution: first column must be Test_Case
                if (col == 0) and (s.cell(row,col).value != ''):
                    testcaseName = s.cell(row,col).value
                    #need to construct a dictionary first
                    testcaseDict[testcaseName] = {}
                    row_start = row

                if s.cell(row,col).value == '':
                    continue

                for firstLevelIdx in range(len(labelInfo)):
                    if labelInfo[firstLevelIdx][1] <= col <= labelInfo[firstLevelIdx][2]:
                        if (labelInfo[firstLevelIdx][1] == col) and (row == row_start):
                            #need to construct a dictionary first
                            testcaseDict[testcaseName][labelInfo[firstLevelIdx][0]]={labelInfo[firstLevelIdx][3][col-labelInfo[firstLevelIdx][1]]:[s.cell(row,col).value]}
                        elif row == row_start:
                            testcaseDict[testcaseName][labelInfo[firstLevelIdx][0]][labelInfo[firstLevelIdx][3][col-labelInfo[firstLevelIdx][1]]] = [s.cell(row,col).value]
                        else:
                            testcaseDict[testcaseName][labelInfo[firstLevelIdx][0]][labelInfo[firstLevelIdx][3][col-labelInfo[firstLevelIdx][1]]].append(s.cell(row,col).value)

            values.append(s.cell(row,col).value)
        print values
    print "sheet: ", s.name
    dictTestcaseSheet[s.name] = testcaseDict

print labelInfo
a =len(labelInfo)
print '\n'.join(testcaseDict)
for tmp_testcase in testcaseDict:
    print '\n' + tmp_testcase + '\n'
    print testcaseDict[tmp_testcase]


srs_wb.cfg_gen(dictTestcaseSheet,caseDir)
srs_nb.cfg_gen(dictTestcaseSheet,caseDir)

print '\nALL TESTCASES HAVE BEEN SUCCESSFULLY GENERATED!'