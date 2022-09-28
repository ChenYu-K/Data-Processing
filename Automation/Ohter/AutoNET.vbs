'Autologin to the network
'Created by: Y.chen 2022-09-27
'Last modified: 2022-09-27

'You Must have an autofill(ID and password) in your browser

'Global variables
Option Explicit

Dim objShell,objFSO, objFolder, bag, pipe
Dim CurrentTime,IE

Set IE = CreateObject("InternetExplorer.Application")
Set objShell = CreateObject("WScript.Shell")
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")
Set objFolder = objFSO.GetFolder(objShell.CurrentDirectory)
set bag=getobject("winmgmts:\\.\root\cimv2") 
set pipe=bag.ExecQuery("select * from win32_process where name='wscript.exe'")

CurrentTime=Hour(Now)&Minute(Now)&Second(Now)
'Msgbox CurrentTime

do

    if pipe.count > 1 then          'Check if the vbs script is run
    Msgbox "do not open again, script is running"
    WScript.Quit
    else

        if CurrentTime = 50000 then    'Check if the time is 5:00:00
            autologin(objFolder)
        end if
    end if

loop


sub autologin(objFolder)
    On Error Resume Next
   
    objshell.Run "chrome.exe https://hms.cii.omu.ac.jp/saibed/LogOut"

    WScript.sleep(30000)

    objShell.Run "ipconfig /release"
    WScript.sleep(10000)
    objShell.Run "ipconfig /renew"
    WScript.sleep(30000)

    objshell.Run "chrome.exe https://webauth.omu.ac.jp/portal/"
    WScript.sleep(10000)
    objShell.SendKeys "{F11}"
    WScript.sleep(1000)
    objShell.SendKeys "{Tab}"
    WScript.sleep(1000)
    objShell.SendKeys "{Tab}"
    WScript.sleep(1000)
    objShell.SendKeys "{ENTER}"
    WScript.sleep(1000)
    objShell.SendKeys "{F11}"
End sub