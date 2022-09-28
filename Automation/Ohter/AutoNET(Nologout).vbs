'Autologin to the network
'Created by: Y.chen 2022-09-27
'Last modified: 2022-09-27

'You Must have an autofill(ID and password) in your browser

'Global variables
Option Explicit

Dim objShell,objFSO, objFolder, bag, pipe,strIP
Dim CurrentTime,IE
Dim objWMIService

'Set objWMIService = Getobject("winmgmts:\\.\root\cimv2")
Set IE = CreateObject("InternetExplorer.Application")
Set objShell = CreateObject("WScript.Shell")
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")
Set objFolder = objFSO.GetFolder(objShell.CurrentDirectory)
set bag=getobject("winmgmts:\\.\root\cimv2") 
set pipe=bag.ExecQuery("select * from win32_process where name='wscript.exe'")

'CurrentTime=Hour(Now)&Minute(Now)&Second(Now)
'Msgbox CurrentTime

strIP="https://www.google.com"

do while true

    if pipe.count > 2 then          'Check if the vbs script is run
        Msgbox "do not open again"
        WScript.Quit
    'elseif Not IsOnline_1(strIP) Then
    elseif CheckConnection(strIP) = 0 then
        autologin(objFolder)
        'Msgbox "no internet"
    end if
    WScript.sleep(1300)
loop


sub autologin(objFolder)
    On Error Resume Next
   
    'objshell.Run "chrome.exe https://hms.cii.omu.ac.jp/saibed/LogOut"

    WScript.sleep(5000)

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

Function IsOnline_1(URLstr)
    Dim strComputer,colPings,objPing

    IsOnline_1 = false

    strComputer = "."

    Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")

    Set colPings = objWMIService.ExecQuery ("Select * From Win32_PingStatus where Address = '" & URLstr & "'")

    For Each objPing in colPings

        if instr(objPing.ProtocolAddress,URLstr)>0 then

            IsOnline_1=true
            exit for

        end if

    Next

End Function

Function CheckConnection(URL)
    On Error Resume Next 'swallow errors
    Dim o

    Set o = CreateObject("MSXML2.XMLHTTP") 
    o.open "GET",URL, False 
    o.send 
    If Err.Number <> 0 Then
        CheckConnection = 0 '"An error occured. Data not retrieved."
'or whatever else you want to do in such a case.
    Else
        CheckConnection = 1 '"You are connected"
    End If
    On Error Goto 0 'back to normal error behaviour
End Function