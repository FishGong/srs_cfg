#-------------------------------------------------------------------------------
# Name:        srs_nb
# Purpose:     generate NB srs bcem fdd cfg
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
import srs_prb_calc
reload(sys)
sys.setdefaultencoding('utf-8')
#(3) generate cfg files default value is given
list_antenna_relativeLocation = [-8, 8, -8, 8, 8, -8, 8, -8]
dict_dlAntenna_cellTopology = {1:0, 2:1, 4:2, 8:3, 6:4, 3:5}
dict_ulAntenna_cellTopology = {1:0, 2:1, 3:2, 4:3, 6:4, 8:5, 12:6}
dict_bandwidth_idx = {1.4:0, 3:1, 5:2, 10:3, 15:4, 20:5}
dict_antenna_mode = {2:0, 4:1, 8:2}
dict_ueid_rnti = {}
#list_ue_rnti = [694, 2302,695,696,697,698,699,700]
dict_idftprb_num = {4:4,8:6,12:8,16:10,20:12,24:16,32:18,36:20,40:24,48:30,60:32,64:36,72:48,80:48,96:50}

srsSubfrmCfg = 1
srsBwCfg = 0
srsMaxUpPts = 0
nCellId = 0
hopbw = 0
strNoTab='\n'
strOneTab='\n   '
strTwoTab='\n      '
strThreeTab='\n         '
strCommentTab = '      '
testCaseDir=''
allocparity = 0
bandwidth = 10
bandwidthIdx = 3
numAnt = 2
num_ue = 1
framenum = 0
sfnum = 8
numprb = 6
startprb = 12

def cfg_gen(dictTestcaseSheet,caseDir):
    print "(3) generate cfg files of all cases in the case list"
    for tcSheet in dictTestcaseSheet:
        if(tcSheet != 'NBSRS'):
            continue
        testcaseDict = {}
        testcaseDict = dictTestcaseSheet[tcSheet]
        tmp_caseDir = caseDir + tcSheet + '\\'
        if os.path.exists(tmp_caseDir):
            shutil.rmtree(tmp_caseDir)
        os.mkdir(tmp_caseDir)
        #print tmp_caseDir
        for testCase in testcaseDict:
            testCaseDir=tmp_caseDir
            print testCaseDir+testCase+'.cfg'
        #print testcaseDict[testCase]
            list_ue_rnti = []
            if testcaseDict[testCase]['Common_Parameters']['Bandwidth'][0] != 'NA':
                bandwidth = int(testcaseDict[testCase]['Common_Parameters']['Bandwidth'][0])
                bandwidthIdx = int(dict_bandwidth_idx[bandwidth])
            if testcaseDict[testCase]['Common_Parameters']['AntNumUl'][0] != 'NA':
                numAnt = int(testcaseDict[testCase]['Common_Parameters']['AntNumUl'][0])
            if testcaseDict[testCase]['Common_Parameters']['NCellId'][0] != 'NA':
                nCellId = int(testcaseDict[testCase]['Common_Parameters']['NCellId'][0])

            #start to write to cfg file
            cfgFile=open(testCaseDir+testCase+'.cfg', 'w')
            strCfgUl = ''

            strCfgUl += strNoTab + '/*----------------------  Globals Section  ------------------------*/' + \
                       strNoTab + 'Globals' + \
                       strOneTab + 'BandWidth              = ' + str(bandwidth) + 'MHz' + \
                       strOneTab + 'StartingSimulationTick = -6' + \
                       strOneTab + 'FixedRandomSeed        = true' + \
                       strOneTab + 'BtsOverSamplingDL      = 1' + \
                       strOneTab + 'ChannelOverSamplingUL  = 1' + \
                       strOneTab + 'ChannelOverSamplingDL  = 2' + \
                       strOneTab + 'CarrierFrequencyUL     = 1900000000' + \
                       strOneTab + 'CarrierFrequencyDL     = 2100000000' + \
                       strOneTab + 'CellRadius             = 50000' + \
                       strOneTab + 'AdcMode                = UCU3'  + \
                       strOneTab + 'LR141Enabled           = true'  + \
                       strOneTab + 'EmifEnabled            = true' + \
                       strOneTab + 'k_RA                   = 3' + \
                       strOneTab + 'RachHistogramOn        = true' + \
                       strOneTab + 'PiCycleTime            = 0' + \
                       strOneTab + 'DumpData' + \
                       strTwoTab + 'DumpTags = enable' +\
                       strNoTab

            strCfgUl += strTwoTab + 'EnableTag = 20' + \
                           strTwoTab + 'EnableTag = 1001' + \
                           strTwoTab + 'EnableTag = 40027' + \
                           strTwoTab + 'EnableTag = 40028' + \
                           strTwoTab + 'EnableTag = 40034' + \
                           strTwoTab + 'EnableTag = 20161' + \
                           strTwoTab + 'EnableTag = 54001' + \
                           strTwoTab + 'TagRange  = 56000 56300' + \
                           strOneTab + 'End (DumpData)' + \
                           strNoTab + 'End Globals' + \
                           strNoTab

            strCfgUl += strNoTab + '/*----------------------  Bts Section  -----------------------*/' + \
                       strNoTab + 'Bts' + \
                       strOneTab + 'AgcMode           = static' + \
                       strOneTab + 'InitialAgcGain    = 25' + \
                       strOneTab + 'NG3NoiseBits      = 2.8' + \
                       strNoTab + \
                       strOneTab + 'SectorInfo' + \
                       strTwoTab + 'CellId         = 0' + \
                       strTwoTab + 'AntennaSetId   = Sect1' + \
                       strTwoTab + 'NumberAntennas = ' + str(numAnt) + \
                       strOneTab + 'End (SectorInfo)' + \
                       strNoTab

            for antenna in range(numAnt):
                strCfgUl += \
                       strOneTab + 'RxBus = ' + str(antenna) + ' Sect1_Ant' + str(antenna+1)


            strCfgUl += strNoTab
            strCfgUl += \
                    strOneTab + 'Column,Antenna,IdStr,GroupId,RelativeLocation,Orientation,PhaseRefXY,RxGain'

            for antenna in range(numAnt):
                strCfgUl += \
                       strOneTab + 'Antenna,   ' + 'Sect1_Ant' + str(antenna+1) +',   Sect1,         ' +  str(list_antenna_relativeLocation[antenna]) + ',     60,   0    0,  1.000 0.000'

            strCfgUl += strNoTab
            strCfgUl += \
            strOneTab + 'FpgaC' + \
            strTwoTab + 'FreqEqualizeLb = 4' + \
            strTwoTab + 'XIArchPipelined = true' + \
            strTwoTab + 'IrcProcessEnabled = true' + \
            strTwoTab + 'NewEqQuantEnabled = true' + \
            strTwoTab + 'SrsAgcAlgoOption = 1 // 0 default, 1, 2 new' + \
            strOneTab + 'End (FpgaC)' +\
            strOneTab + 'DspA' + \
            strTwoTab + 'DeliverCfgsTogether = true' + \
            strTwoTab + 'DspResetEnabled = true'   + \
            strTwoTab + 'UseFreescaleTurboDecoder = true' + \
            strTwoTab + 'UseFreescaleDft = true' + \
            strTwoTab + 'EnableSrsNoiseEstUsingMinCyclicShift = true' + \
            strTwoTab + 'AlignLtAvgSoc = true' + \
            strTwoTab + 'AlignLtNoiseSoc = true' +\
            strOneTab + 'End (DspA)' + \
            strNoTab + 'End - Bts' + \
            strNoTab

            strCfgUl += strNoTab + '/*------------------ Ue Section  --------------------*/'
            for item in range(len(testcaseDict[testCase]['Schedule']['UeID'])):
                ue_id = int(testcaseDict[testCase]['Schedule']['UeID'][item])
                ue_rnti = int(testcaseDict[testCase]['Schedule']['Rnti'][item])
                if not((ue_id,ue_rnti) in list_ue_rnti):
                    list_ue_rnti.append((ue_id,ue_rnti))

            num_ue = int(testcaseDict[testCase]['Common_Parameters']['NumUe'][0])
            for ue in range(num_ue):
                if (1 == int(testcaseDict[testCase]['Schedule']['GrpHopping'][ue])):
                    grphop = 'true'
                else:
                    grphop = 'false'
                strCfgUl += \
                       strNoTab + 'Ue' + \
                       strOneTab + 'Number = ' + str(ue) + \
                       strOneTab + 'IdStr  = Ue' + str(ue+1) + \
                       strOneTab + 'UeAntennaSetId = Ue' + str(ue+1) + \
                       strOneTab + 'SpeedKph = 0' + \
                       strOneTab + 'Direction = 0' + \
                       strOneTab + 'InitialLocation -707 707' + \
                       strOneTab + 'TxEnabled  true' + \
                       strOneTab + 'NCellID = ' + str(nCellId) + \
                       strOneTab + 'RNTI = ' + str(list_ue_rnti[ue][1]) + \
                       strOneTab + 'GroupHopping ' + grphop + \
                       strOneTab + 'FrequencyOffset   = 0' + \
                       strNoTab + 'End (Ue ' + str(ue+1) + ')' + \
                       strNoTab
            strCfgUl += strNoTab + '/*---------------------- Channel Section ---------------------*/' + \
                    strNoTab
            for ue in range(num_ue):
                channelDelay = int(bandwidth*3.6)
                strCfgUl += \
                       strNoTab + 'WireChannel' + \
                       strOneTab + 'Id = Sect1:Ue' + str(ue+1) + \
                       strOneTab + 'BtsAntennaSetId = Sect1' + \
                       strOneTab + 'UeAntennaSetId  = Ue' + str(ue+1) + \
                       strOneTab + '//ChannelDelayInNibs  = ' + str(channelDelay) + \
                       strNoTab + 'End' + \
                       strNoTab

            strCfgUl += strNoTab + '/*---------------------- Schedule Section --------------------*/' + \
                       strNoTab + 'Schedule' + \
                       strOneTab + 'DspInitRequest' + \
                       strTwoTab + 'AbsoluteTick -4' + \
                       strOneTab + 'End' + \
                       strNoTab + \
                       strNoTab + 'CeConfigRequest' + \
                       strOneTab + 'AbsoluteTick -3' + \
                       strNoTab + 'End' + \
                       strNoTab + \
                       strNoTab + 'CLtgConfigMsg' + \
                       strOneTab + 'AbsoluteTick     -4' + \
                       strOneTab + 'CellIdx        = 0' + \
                       strOneTab + 'AntMode = ' + str(dict_antenna_mode[numAnt]) + \
                       strOneTab + 'AntsEnableMask = 3' + \
                       strOneTab + 'EnergySelect   = 0' + \
                       strOneTab + 'TocSelect      = 1' + \
                       strOneTab + 'NvarSelect     = 0' + \
                       strNoTab + 'End' + \
                       strNoTab
            tick_list = []
            couple = []
            lense = len(testcaseDict[testCase]['Schedule']['UeID'])

            if(num_ue == 1):
                num_nb_srs = 0
            else:
                num_nb_srs = num_ue
            strCfgUl += strNoTab + '/*------- schedule LRX Section ----*/' + \
                       strNoTab + \
                       strNoTab + 'Column,LrxConfigMsg,AbsoluteTick, DeltaTick, Repeat, CellIdx,Num_SRS,Num_Nb_SRS' + \
                       strNoTab

            strCfgUl += strNoTab + 'LrxConfigMsg,                 -5,  16,       -1,         0,      1,         ' + str(num_nb_srs)

            strCfgUl += strNoTab + \
                strNoTab + 'Column,LrxCellConfigMsg,AbsoluteTick,DeltaTick, Repeat,CellEnabled,NumofUsers,CellIdx,NumofDbgPrbs, NumofPucPrbs, FFTPucPrb0, FFTPucPrb1, FFTPucPrb2, FFTPucPrb3, PucTypPrb0, PucTypPrb1, PucTypPrb2, PucTypPrb3'

            strCfgUl += strNoTab + 'LrxCellConfigMsg,     -4,        16,    500,        true,     ' + str(num_ue) + ',      0,     0,           4,           0,              1,           '+ str(srs_prb_calc.BwIdxMaxPrbs[bandwidthIdx]-2) + ',              ' + str(srs_prb_calc.BwIdxMaxPrbs[bandwidthIdx]-1) + ',           0,          0,          0,            0'
            strCfgUl += strNoTab
            strCfgUl += \
                strNoTab + 'Column,LrxSrsConfigMsg,AbsoluteTick,DeltaTick, Repeat, Index,CellIdx,GrpIndex,StartPRB,NumofPRBs,NumOfPrbIdft,NumOfUsers,RepFactor,CombSelect,SrsAgcMode,AllocParity,Srs_band_idx,nRRCSrs,GrpHopping,NcellID'
            for ue in range(num_ue):
                bsrs = int(testcaseDict[testCase]['Schedule']['Bsrs'][ue])
                csrs = int(testcaseDict[testCase]['Common_Parameters']['Csrs'][0])
                bwidx = bandwidthIdx
                (tsrs,toffset) = srs_prb_calc.srs_map(int(testcaseDict[testCase]['Schedule']['Isrs'][ue]))
                nrrc = int(testcaseDict[testCase]['Schedule']['nrrc'][ue])
                hopbw = int(testcaseDict[testCase]['Schedule']['NbHopBW'][ue])
                ktc = int(testcaseDict[testCase]['Schedule']['CombSelect'][ue])

                (startprb,numprb,srsbwidx) = srs_prb_calc.srs_prb_calc(bsrs,csrs,bwidx,tsrs,nrrc,hopbw,ktc,toffset)
                idftnrb = dict_idftprb_num[numprb]
                cycicshift = int(testcaseDict[testCase]['Schedule']['Cycic Shift'][ue])
                grphop = int(testcaseDict[testCase]['Schedule']['GrpHopping'][ue])
                if cycicshift/2 == 1:
                    allocparity = 1
                else:
                    allocparity = 0

                strCfgUl += strNoTab + 'LrxSrsConfigMsg,                 ' + str(toffset*16 - 4) + ',     ' + str(16*tsrs) + ',     500,   ' + str(ue) + ',      0,       0,      ' + str(startprb)+ ',          ' + str(numprb) + ',        ' + str(idftnrb) + ',         ' + str(num_ue) +',        1,         ' + \
                    str(ktc) + ',         4,          ' + str(allocparity) + ',       ' + str(srsbwidx) + ',       ' + str(nrrc) + ',         '  + str(grphop) + ',         ' + str(nCellId)

            strCfgUl += \
                strNoTab + 'Column,LrxSrsUserConfigMsg,AbsoluteTick, DeltaTick, Repeat, Index,Epsilon,UserId,CyclicShift,SrsNbHopping,SrsSubframe,SrsTransPeriod'
            for u in range(num_ue):
                cycicshift = int(testcaseDict[testCase]['Schedule']['Cycic Shift'][u])
                (tsrs,toffset) = srs_prb_calc.srs_map(int(testcaseDict[testCase]['Schedule']['Isrs'][u]))

                strCfgUl += \
                    strNoTab + 'LrxSrsUserConfigMsg,                 ' + str(toffset*16 - 4) + ',     ' + str(16*tsrs) + ',    500,    ' + str(u) + ',      0,     ' + str(u) + ',          ' + str(cycicshift) + ',          1,         1,             ' + str(tsrs)
            for i in range(num_ue):
                bsrs = int(testcaseDict[testCase]['Schedule']['Bsrs'][i])
                csrs = int(testcaseDict[testCase]['Common_Parameters']['Csrs'][0])
                (tsrs,toffset) = srs_prb_calc.srs_map(int(testcaseDict[testCase]['Schedule']['Isrs'][i]))

                nrrc = int(testcaseDict[testCase]['Schedule']['nrrc'][i])
                hopbw = int(testcaseDict[testCase]['Schedule']['NbHopBW'][i])
                ktc = int(testcaseDict[testCase]['Schedule']['CombSelect'][i])
                cycicshift = int(testcaseDict[testCase]['Schedule']['Cycic Shift'][i])
                (startprb,numprb,srsbwidx) = srs_prb_calc.srs_prb_calc(bsrs,csrs,bandwidthIdx,tsrs,nrrc,hopbw,ktc,toffset)
                strCfgUl += strNoTab + 'UeCommand ' + str(i) + \
                     strOneTab +'AbsoluteTick  ' + str(toffset*16) + \
                     strOneTab + 'DeltaTick    ' + str(16*tsrs) + \
                     strNoTab + \
                     strOneTab + 'ConfigSrs' + \
                     strTwoTab + 'SrsPosition         = LAST_SYMBOL' +\
                     strTwoTab + 'SrsNumPrb           = ' + str(numprb) + \
                     strTwoTab + 'PrbStartLocation    = ' + str(startprb) + \
                     strTwoTab + 'Comb                = ' + str(ktc) + \
                     strTwoTab + 'CyclicShift         = ' + str(cycicshift) +\
                     strTwoTab + 'Duration            = 1' + \
                     strTwoTab + 'TransmissionPeriod  = ' + str(tsrs) + \
                     strTwoTab + 'SubframeOffset      = ' + str(toffset) + \
                     strTwoTab + 'BetaSrs             = 0.39388' + \
                     strTwoTab + 'SrsFreqHopping      = 1' + \
                     strTwoTab + 'nRRC = ' + str(nrrc) + \
                     strOneTab + 'End' + \
                     strNoTab + 'End'
            strCfgUl += strNoTab + 'End (Scheduler)'
            cfgFile.write(strCfgUl)
            cfgFile.close()
    return



