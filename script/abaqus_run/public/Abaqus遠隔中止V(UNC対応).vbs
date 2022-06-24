Option Explicit
Dim objShell, objFolder, objFSO, objFile1, path, r1,over

Set objShell = CreateObject("WScript.Shell")
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")
Set objFolder = objFSO.GetFolder(objShell.CurrentDirectory)

path = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path

r1 = "C:\Windows\System32\cmd.exe /k pushd " & path
objShell.run r1
WScript.Sleep( 500 )

For Each objFile1 In objFolder.Files
	If Right(objFile1.Name, 4)=".inp" Then
		objShell.SendKeys "abaqus terminate job=" & Replace(objFile1.Name, ".inp", "")
		objShell.SendKeys( "{ENTER}" )
	End If
Next

WScript.Sleep( 10000 )
objShell.SendKeys( "popd" )
objShell.SendKeys( "{ENTER}" )
WScript.Sleep( 10000 )
objShell.SendKeys( "echo The job has been terminated you can close this CMD" )
objShell.SendKeys( "{ENTER}" )
WScript.Sleep( 10000 )
objShell.SendKeys( "popd" )
objShell.SendKeys( "{ENTER}" )

