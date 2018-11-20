#-------------------------------------------------------------------------------
# Name:        srs_prb_calc
# Purpose:
#
# Author:      jegong
#
# Created:     29/06/2017
# Copyright:   (c) jegong 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Embedded file name: D:\User\jegong\Desktop\srs_cfg\srs_prb_calc.py
m_SRS_table = [

  [
    [36, 12, 4,  4],
    [32, 16, 8,  4],
    [24, 4,  4,  4],
    [20, 4,  4,  4],
    [16, 4,  4,  4],
    [12, 4,  4,  4],
    [8,  4,  4,  4],
    [4,  4,  4,  4]
  ],

  [
    [48, 24, 12, 4],
    [48, 16, 8,  4],
    [40, 20, 4,  4],
    [36, 12, 4,  4],
    [32, 16, 8,  4],
    [24, 4,  4,  4],
    [20, 4,  4,  4],
    [16, 4,  4,  4]
  ],

  [
    [72, 24, 12, 4],
    [64, 32, 16, 4],
    [60, 20, 4,  4],
    [48, 24, 12, 4],
    [48, 16, 8,  4],
    [40, 20, 4,  4],
    [36, 12, 4,  4],
    [32, 16, 8,  4]
  ],


  [
    [96, 48, 24, 4],
    [96, 32, 16, 4],
    [80, 40, 20, 4],
    [72, 24, 12, 4],
    [64, 32, 16, 4],
    [60, 20, 4,  4],
    [48, 24, 12, 4],
    [48, 16, 8,  4]
  ]
]
N_b_table = [

  [
    [1, 3, 3, 1],
    [1, 2, 2, 2],
    [1, 6, 1, 1],
    [1, 5, 1, 1],
    [1, 4, 1, 1],
    [1, 3, 1, 1],
    [1, 2, 1, 1],
    [1, 1, 1, 1]
  ],

  [
    [1, 2, 2, 3],
    [1, 3, 2, 2],
    [1, 2, 5, 1],
    [1, 3, 3, 1],
    [1, 2, 2, 2],
    [1, 6, 1, 1],
    [1, 5, 1, 1],
    [1, 4, 1, 1]
  ],

  [
    [1, 3, 2, 3],
    [1, 2, 2, 4],
    [1, 3, 5, 1],
    [1, 2, 2, 3],
    [1, 3, 2, 2],
    [1, 2, 5, 1],
    [1, 3, 3, 1],
    [1, 2, 2, 2]
  ],


  [
    [1, 2, 2, 6],
    [1, 3, 2, 4],
    [1, 2, 2, 5],
    [1, 3, 2, 3],
    [1, 2, 2, 4],
    [1, 3, 5, 1],
    [1, 2, 2, 3],
    [1, 3, 2, 2]
  ]
]
FddUeSrsPeriodicity = [
    [    0,    1,    2,    0],
    [    2,    6,    5,    2],
    [    7,  16,   10,    7],
    [  17,   36,   20,   17],
    [  37,   76,   40,   37],
    [  77,  156,  80,   77],
    [ 157, 316,  160,  157],
    [ 317, 636,  320,  317],
    [ 637, 1023,   0,    0]
]
BwIdxMaxPrbs = [6,
 15,
 25,
 50,
 75,
 100]
M_SC_RS = [-1,
 -1,
 -1,
 -1]
n = [-1,
 -1,
 -1,
 -1]

def srs_map(Isrs):
    for i in range(0, 9):
        if Isrs >= FddUeSrsPeriodicity[i][0] and Isrs <= FddUeSrsPeriodicity[i][1]:
            t_srs = FddUeSrsPeriodicity[i][2]
            t_offset = Isrs - FddUeSrsPeriodicity[i][3]
            break

    return (t_srs, t_offset)


def srs_prb_calc(bsrs, csrs, bwidx, tsrs, nrrc, hopbw, ktc, sfidx):
    max_prb = BwIdxMaxPrbs[bwidx]
    if max_prb >= 6 and max_prb <= 40:
        BwWidthIdx = 0
    elif max_prb >= 40 and max_prb <= 60:
        BwWidthIdx = 1
    elif max_prb >= 60 and max_prb <= 80:
        BwWidthIdx = 2
    else:
        BwWidthIdx = 3
    NumPrb = m_SRS_table[BwWidthIdx][csrs][bsrs]
    for i in range(0, bsrs + 1):
        m_srs_b = m_SRS_table[BwWidthIdx][csrs][i]
        N_b = N_b_table[BwWidthIdx][csrs][i]
        M_SC_RS[i] = m_srs_b * 12 / 2
        n_SRS = 0
        if tsrs == 0:
            n_SRS = 0
        else:
            n_SRS = sfidx / tsrs
        if hopbw >= bsrs:
            n[i] = 4 * nrrc / m_srs_b % N_b
        elif i <= hopbw:
            n[i] = 4 * nrrc / m_srs_b % N_b
        else:
            tmpMul_1 = 1
            tmpMul_2 = 1
            for j in range(hopbw, i + 1):
                tmpNb = N_b_table[BwWidthIdx][csrs][j]
                if j == hopbw:
                    tmpNb = 1
                tmpMul_1 *= tmpNb
                if j == i - 1:
                    tmpMul_2 = tmpMul_1

            if N_b % 2 == 0:
                Tmp1 = n_SRS % tmpMul_1
                F_b = N_b / 2 * (Tmp1 / tmpMul_2) + Tmp1 / 2 / tmpMul_2
            else:
                F_b = N_b / 2 * (n_SRS / tmpMul_2)
            n[i] = (F_b + 4 * nrrc / m_srs_b) % N_b


    m_SRS_0 = m_SRS_table[BwWidthIdx][csrs][0]
    k0 = max_prb / 2 - m_SRS_0 / 2
    k0 = k0 * 12 + ktc
    tempK = 0
    for m in range(0, bsrs + 1):
        tempK += 2 * M_SC_RS[m] * n[m]
    srsbwidx = n[bsrs]
    k0 += tempK
    Startprb = k0 / 12
    return (Startprb, NumPrb,srsbwidx)
