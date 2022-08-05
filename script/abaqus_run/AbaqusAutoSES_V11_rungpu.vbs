'Original file was created by Takai, V7~ Update and Modify by yu chen. 
'Copyright@2022 Osaka Metroplitan University Bridge Engieering Lab
'License: Apache License Version 2.0, January 2004 http://www.apache.org/licenses/
'Update time is 2022.6.22
'The project was pu on the https://github.com/ChenYu-K/Data-Processing/tree/main/script/abaqus_run/test
'Update logfile was uploaded in github

Option Explicit

Dim objShell, objFSO
Dim objFolder, objFile1, objFile2, strFile3
Dim intCPU, intThread
Dim intI, intJ, intK, strNow

intCPU=8     '計算時のCPU数を「intCPU=」のあとに半角数字で書く（1、2、4、8とか；4推奨）
intThread=1  '同時に計算する本数を「intThread=」のあとに半角数字で書く（1、2、3とか；1推奨）

Set objShell = CreateObject("WScript.Shell")
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")

Set objFolder = objFSO.GetFolder(objShell.CurrentDirectory)

Set objFile1 = objFSO.OpenTextFile("Abaqus自動直列実行_停止方法.txt", 2, True)
objFile1.WriteLine "***スクリプトの停止方法***"
objFile1.WriteLine " このファイル「Abaqus自動直列実行_停止方法.txt」を削除する.(5秒程度で停止)"
objFile1.WriteLine " "
objFile1.WriteLine "***スクリプトの使い方（計算実行）***"
objFile1.WriteLine " 1. スクリプトファイルを任意のフォルダーにコピーする."
objFile1.WriteLine " ファイル名「Abaqus自動直列実行_name.vbs」"
objFile1.WriteLine " 2. スクリプトを実行する."
objFile1.WriteLine " 3. 「～.inp」ファイルをこのフォルダーにコピーする."
objFile1.WriteLine " 4. 計算が終わるまで待つ."
objFile1.WriteLine " 5. 計算が終わったら「Finished_～」のフォルダーごと自分の個人フォルダーに移動する."
objFile1.WriteLine " *** スクリプト処理の流れ"
objFile1.WriteLine "   「～.inp」ファイルがあれば,「_queued_～.inp」にファイル名変更"
objFile1.WriteLine "	 →計算投入を待つ"
objFile1.WriteLine "	 →「_queued_～.inp」の名前順に「～.inp」ファイルを戻して計算投入"
objFile1.WriteLine "	 →計算が終了すれば「Finished_～」のフォルダを作成し結果ファイルを移動"
objFile1.WriteLine "		...この繰返し"
objFile1.WriteLine "	* 「_queued_～.inp」に変更することでファイルを認識した時刻順に並べています."
objFile1.WriteLine " 	* Abaqusトークンが不足すると計算投入直後に計算待ちになります."
objFile1.WriteLine "	* このスクリプトの機能は，時期をみて計算投入するだけなので，"
objFile1.WriteLine "	* スクリプトを停止しても, Abaqusの計算は継続されます."
objFile1.WriteLine "	* inpファイルがない状態でこのスクリプトを実行しても特に何も起きません."
objFile1.WriteLine " "
objFile1.WriteLine "***スクリプトの使い方（設定編）***"
objFile1.WriteLine " スクリプトをスタートアップに登録しておくと，スクリプト起動の手間が省けます．"
objFile1.WriteLine " 「abaqus anasysis」で計算投入するため, どのバージョンで計算されるかは，"
objFile1.WriteLine "  その端末のabaqus.batの設定によります."
objFile1.WriteLine " "
objFile1.Close

Do

	If objFSO.FileExists("Abaqus自動直列実行_停止方法.txt") = False Then
		objShell.Popup "スクリプトが停止しました", 4, "Abaqus自動直列実行"
		WScript.Quit
	End If
	queueLoop(objFolder)
	WScript.sleep(5000)	 ' change the 500ms to 5000ms,that for Waiting for the .log to finish reading and writing status.
	finishLoop(objFolder)
	WScript.sleep(2000)	'delated the for loop and change the time to 2s

    
	executeLoop(objFolder)
Loop


Sub queueLoop(objFolder)
	On Error Resume Next
	For Each objFile1 In objFolder.Files
		If Right(objFile1.Name, 4)=".inp" and Left(objFile1.Name, 8)<>"_queued_" and objFSO.FileExists(Replace(objFile1.Name, ".inp", ".log")) = False Then
			objFSO.MoveFile objFile1, objFile1.ParentFolder & "\_queued_" & Year(Now) & right("0" & Month(Now), 2) & right("0" & Day(Now), 2) & "_" & right("0" & Hour(Now), 2) & right("0" & Minute(Now), 2) & right("0" & Second(Now), 2) & "_" &  objFile1.Name
			Exit Sub
		End If
	Next
End Sub

Sub finishLoop(objFolder)
	On Error Resume Next
	For Each objFile1 In objFolder.Files
		If Right(objFile1.Name, 4)=".odb" and objFSO.FileExists(Replace(objFile1.Name, ".odb", ".lck")) = False and objFSO.FileExists(Replace(objFile1.Name, ".odb", ".com")) = True Then
			WScript.sleep(10000) 'add wait time to wait the log file over the writing status.
			strFile3 = objFile1.Name
			strNow = Year(Now) & right("0" & Month(Now), 2) & right("0" & Day(Now), 2) & "_" & right("0" & Hour(Now), 2) & right("0" & Minute(Now), 2) & right("0" & Second(Now), 2) 
			objFSO.CreateFolder(objFolder & "\Finished_" & strNow & "_" & Replace(objFile1.Name, ".odb", ""))

			For Each objFile2 In objFolder.Files
				If InStr(objFile2, Replace(strFile3, ".odb", "")) > 0 and Left(objFile2.name,8)<>"_queued_" Then
					objFSO.MoveFile objFile2, "Finished_" & strNow & "_" & Replace(strFile3, ".odb", "") & "\"
				End If
			Next
        End If
	Next
End Sub

Sub executeLoop(objFolder)
	'指定個(intThread)計算中なら新たに実行しない
	intI=0
	For Each objFile1 In objFolder.Files
		If Right(objFile1.Name, 4)=".log" Then 'change .lck to .log, to prevent .lck from appearing too slow, cause abaqus calculate 2 inp at the same time.
			intI=intI+1
		End If
	Next
	If intI >= intThread Then
		Exit Sub
	End If

	'実行する
	intJ=0
	For Each objFile1 In objFolder.Files
		If intJ >= intThread - intI Then
			Exit For
		End If
		If Right(objFile1.Name, 4)=".inp" and Left(objFile1.Name, 8)="_queued_" Then
			strFile3 = Right(objFile1.Name, Len(objFile1.Name) - 24)
			objFSO.MoveFile objFile1, strFile3
			objShell.Run "abaqus job=" & Replace(strFile3, ".inp", "") & " cpus=" & intCPU & " gpus=1 ask_delete=OFF"
			WScript.sleep(13000) 'change time to 15s
			intJ = intJ + 1
		End If
        If intJ >= intThread - intI Then
            Exit For
		End If
	Next
End Sub

Function GetFileTitle(sFileName)        'Function without extension name
    Dim pos
    pos = InStrRev(sFileName, ".")      'Search for substrings from the end of the string forward(".")
    if(pos = 0) Then                    'file have not extension_name
        GetFileTitle = sFileName
    else
        GetFileTitle = Left(sFileName, pos - 1)
    end if
End Function
