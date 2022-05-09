#*-* encoding: utf-8 *-*
import os, re
import chardet
import subprocess
import unicodecsv as csv
import numpy as np
import pandas as pd 
import re
from pandas.plotting import  table
import matplotlib.pyplot as plt
import dataframe_image as dfi
import time

while True:
    time.sleep(40)
    nowis=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) #nowtime

    obj = subprocess.Popen(["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
    obj.stdin.write("abaqus licensing dslsstat -usage")
    obj.stdin.write("\n")
    obj.stdin.close()

    cmd_out = obj.stdout.read()
    obj.stdout.close()
    cmd_error = obj.stderr.read()
    obj.stderr.close()

    cmd_out2 = cmd_out.splitlines()
    #cmd_out2 = cmd_out2.split('|')

    out3 = np.array(cmd_out2).T

    df=pd.DataFrame(out3)
    df=df[0].str.split('|', expand=True)
    df1=df[0].str.split(',', expand=True)
    df1[['a','b','c','day','Start_time','f','License','h']]=df1[1].str.split('\s', expand=True)
    #df=pd.concat([df1,df2], axis=1)
    df=df1.drop(df1.tail(2).index) #从末尾からn行を消す

    ######################################
    for idx in reversed(df.index): #末尾から数える，noneがあれば止まる
        if df.loc[idx,'License'] == None :
            break
    df5=df.drop(df.head(idx).index) #最後ライセンスの何行を残す
    ################################

    df5=df5.drop([1,'a','b','c'], axis=1)
    df5['License'] = df5['License'].fillna(0).astype(int) #remove none and to int

    ###########################################
    df6=df5.groupby([0,'Start_time'], sort=False)['License'].sum().reset_index()    #時間同じ行のlICENSEを足し合わせる
    lisum=df6['License'].sum()          #現在実行中の総使用量
    remin='remaing:'+str(620-lisum)        #残量
    alllisen='************Update time is :'+str(nowis)+'************'
    lisen=str(lisum)+'/620'
    df6.loc[df6.index.max() + 1]=[alllisen,remin,lisen]
    df6=df6.rename(columns={0:'PC_name'}) #rename
    #print(df6)
    #########################
    #グラフ化
    #########################
    # fig = plt.figure(figsize=(3, 4), dpi=1400)
    # ax = fig.add_subplot(111, frame_on=False) 
    # ax.xaxis.set_visible(False)  # hide the x axis
    # ax.yaxis.set_visible(False)  # hide the y axis
    # table(ax, df6, loc='center')  #
    #plt.savefig('license.png')
    df_styled = df6.style.background_gradient()
    dfi.export(df_styled,".\lisence.png") #brwikiに保存する
    #df6.to_csv('result.csv')
    # "V:\wiki\public\images\lisence.png"