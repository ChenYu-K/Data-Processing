# *-* encoding: utf-8 *-*
import os
import chardet
import subprocess
import unicodecsv as csv
import numpy as np
import pandas as pd
import re
from pandas.plotting import table
import matplotlib.pyplot as plt
import dataframe_image as dfi
import time

# while True:
#    time.sleep(40)
nowis = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # nowtime

obj = subprocess.Popen(["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True, encoding="utf-8")
obj.stdin.write("abaqus licensing dslsstat -usage")
obj.stdin.write("\n")
obj.stdin.close()

cmd_out = obj.stdout.read()
obj.stdout.close()
cmd_error = obj.stderr.read()
obj.stderr.close()

cmd_out2 = cmd_out.splitlines()
# cmd_out2 = cmd_out2.split('|')

out3 = np.array(cmd_out2).T

df = pd.DataFrame(out3)
df = df[0].str.split('|', expand=True)
df1 = df[0].str.split(',', expand=True)
df1[['a', 'b', 'c', 'day', 'Start_time', 'f', 'License', 'h']] = df1[1].str.split('\s', expand=True)
# df=pd.concat([df1,df2], axis=1)
df = df1.drop(df1.tail(2).index)  # 从末尾からn行を消す

# 誰も使っていないことを確認する
if df['License'].isnull().all():
    info={'Info':['No one is using the license.']}
    info_styled = info.style.background_gradient()
    # dfi.export(indo_styled,"Z:\wiki\public\images\caelisence.png")
    exit()
else:
    ######################################
    for idx in reversed(df.index):  # 末尾から数える，noneがあれば止まる
        if df.loc[idx, 'License'] == None:
            break
    df5 = df.drop(df.head(idx).index)  # 最後ライセンスの何行を残す
    ################################

    df5 = df5.drop([1, 'a', 'b', 'c'], axis=1)
    df5['License'] = df5['License'].fillna(0).astype(int)  # remove none and to int

    ###########################################
    df6 = df5.groupby([0, 'day', 'Start_time'], sort=False)['License'].sum().reset_index()  # 時間同じ行のlICENSEを足し合わせる
    lisum = df6['License'].sum()  # 現在実行中の総使用量
    remin = str(638 - lisum)  # 残量
    alllisen = '************Update time is :' + str(nowis) + '************'
    lisen = str(lisum) + '/638'
    df6.loc[df6.index.max() + 1] = [alllisen, 'Reaming is', remin, lisen]
    df6 = df6.rename(columns={0: 'PC_name'})  # rename
    # print(df6)
    #########################
    # グラフ化
    #########################
    df_styled = df6.style.background_gradient()
    print(df6)
    # dfi.export(df_styled,"Z:\wiki\public\images\lisence.png") #brwikiに保存する
    ############################
    # CAE_License
    ###########################
    ###################################### 最初から数え，Licenseが現れるまでのデータを全部消す

    for idx in df.index:
        if df.loc[idx, 'License'] != None:
            break
    dfpc = df.drop(df.head(idx).index)

    ####################### 新しいdfpcのLicenseを数え，Noneになったらまとめる.
    for idc in dfpc.index:
        if dfpc.loc[idc, 'License'] == None:
            break
    dfpc = dfpc.head(idc - idx)
    dfpc = dfpc.drop([1, 'a', 'b', 'c', 'f', 'h'], axis=1)
    dfpc['License'] = dfpc['License'].fillna(0).astype(int)  # remove none and to int
    ################################
    lisumpc = dfpc['License'].sum()  # 現在実行中の総使用量
    reminpc = str(8 - lisumpc)  # 残量
    alllisenpc = '************Update time is :' + str(nowis) + '************'
    lisenpc = str(lisumpc) + '/8'
    dfpc.loc['Message'] = [alllisenpc, 'Reaming is', reminpc, lisenpc]
    dfpc = dfpc.rename(columns={0: 'PC_name_CAE_License'})  # rename

    #################################
    ####### Replace the pcname ######
    #################################

    for index, row in dfpc.iterrows():
        if "BRADONA" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Sekimoto'
        if "36081" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Rai'
        if "BRONCHI" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Yamada'
        if "BREEZE" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Yasuda'
        if "BRACK" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Takagi'
        if "BRZ-STI" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Kiyama'
        if "BRASKE" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Ishikuro!'
        if "BRSUGA" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Akahoshi'
        if "BREWER" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Qian'
        if "BRAKB" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + '_Zou'
        if "BRHOPE" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + '_Konishi'
        if "BRMESSI" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + '_Komura'
        if "BRACEUP" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:15] + '_M.Ikeda'
        if "BRAWN" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + '_Obaishi'
        if "BRTAEHYUNG" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:10] + 'Jack.Li'
        if "BRONALDINHO" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'T.Hashimoto'
        if "BROMINE" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Hiraoka'
        if "BRKOOK" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Fukutsuji'
        if "BRJIMIN" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Ishiken'
        if "BREAK" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Horii'
        if "BRGOD" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:14] + 'Sakura'
        if "BRCY" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:12] + '_Y.Chen'
        if "BRACE" in dfpc.PC_name_CAE_License[index]:
            dfpc.PC_name_CAE_License[index] = dfpc.PC_name_CAE_License[index][:13] + 'Shirai'

    #########################
    # Output_fig #########
    #########################

    dfpc_styled = dfpc.style.background_gradient()
    print(dfpc)
    # dfi.export(dfpc_styled,"Z:\wiki\public\images\caelisence.png")
