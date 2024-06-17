import os
import datetime
import time
import shutil
import subprocess

#Copyright@2022 Osaka Metroplitan University Bridge Engieering Lab Yu Chen
#License: Apache License Version 2.0, January 2004 http://www.apache.org/licenses/
#Update time is 2023.1.27
#The project was pu on the https://github.com/ChenYu-K/Data-Processing/tree/main/script/abaqus_run/test
#Update logfile was uploaded in github


def timenow():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%m%d%H%M')
    return d

def movefile(mfn,fns):
    for fn in fns:
        if fn[:-3] == mfn:
            shutil.move()

def queueloop(path):
    fns=os.listdir(path)
    for fn in fns:
        if fn.endswith('.inp') and fn[:8] != '_queued_' and (fn[:-3]+'com' in fns) is False:
            newname='_queued_'+timenow()+'-'+fn
            os.rename(fn,newname)

def finishrun(path):
    fns=os.listdir(path)
    for fn in fns:
        if fn.endswith('.odb') and (fn[:-3]+'lck' in fns) is False :
            foldername='./Finished-'+timenow()+'-'+fn[:-3]+'/'
            os.makedirs(foldername)
            time.sleep(5)
            
            for fn1 in fns:
                if fn1[:-3] == fn[:-3] :
                    fn2 = 'Finished-'+ timenow()+'-'+ fn1
                    shutil.move(fn1, foldername+fn2)

def execute(path):
    fns=os.listdir(path)
    for fn in fns:
        if fn.endswith('.inp') and fn[:8]=='_queued_' :
            fn2 = fn[17:]
            os.rename(fn,fn2)
            command = 'abaqus job=%s cpus=1 ask_delete=OFF' %(fn2[:-4])
            subprocess.call(command, shell=True)
            time.sleep(30)
            break

if __name__=='__main__':
    while True:
        path = os.getcwd()
        queueloop(path)
        finishrun(path)
        execute(path)
