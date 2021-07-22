from glob import glob
import csv
from collections import namedtuple
import numpy as np

path = '\\\\10.108.51.13\\sdb\\CHEN\\陳\\1.研究\MatLab\\小型試験データ整理\\'
names = glob(f'{path}*.csv')
cos = np.empty([55,1])
cof = np.empty([55,1])
j = 1
Pslip = 0
Nmax = 0
for name in names:
    with open(name) as f:
        f_csv = csv.reader(f)
        data = list(f_csv)
        a = np.array(data,dtype=object)
        x = range(np.shape(a)[0])
        y = len(data) - 1
    i = 22
    s = 0
    af = np.empty([y,5],dtype = float)
    while i < y :
        af[i,1] = np.abs(float(a[i][4]))    #clamping force
        af[i,2] = np.abs(float(a[i][3]))    #load
        af[i,3] = float(a[i][5])    #disp 1
        af[i,4] = float(a[i][6])    #disp 2
        af[i,0] = 0.5*(np.abs(af[i,4])+np.abs(af[i,3]))   #disp avrege
        if af[i,0] < 1:          #Find Pslip
            if Nmax < af[i,1] : Nmax = af[i,1]          #max clamping force
            if Pslip < af[i,2] :        #slip　judgement
                Pslip = af[i,2]        #max slip load or 1mm slip load
                s += 1
        i += 1

    cos[j] = Pslip / (2*Nmax)
    cof[j] = af[s,2] / (2*Nmax)
    print('分析ケース＝', name)
    print('すべり荷重＝', Pslip)
    print('すべり係数＝', cof[j])
    print('摩擦係数＝', cos[j])
    j += 1
    

