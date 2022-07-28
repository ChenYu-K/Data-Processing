'Original file was created by Takai, V7~ Update and Modify by yu chen. 
'Copyright@2022 Osaka Metroplitan University Bridge Engieering Lab
'License: Apache License Version 2.0, January 2004 http://www.apache.org/licenses/
'Update time is 2022.6.22
'The project was pu on the https://github.com/ChenYu-K/Data-Processing/tree/main/script/abaqus_run/test
'Update logfile was uploaded in github

Option Explicit

Dim objShell, objFSO
Dim objFolder, objFile1, objFile2, strFile3, strFile2
Dim intCPU, intThread
Dim intI, intJ, intK, strNow

intCPU=4     '�v�Z����CPU�����uintCPU=�v�̂��Ƃɔ��p�����ŏ����i1�A2�A4�A8�Ƃ��G4�����j
intThread=1  '�����Ɍv�Z����{�����uintThread=�v�̂��Ƃɔ��p�����ŏ����i1�A2�A3�Ƃ��G1�����j

Set objShell = CreateObject("WScript.Shell")
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")

Set objFolder = objFSO.GetFolder(objShell.CurrentDirectory)

Set objFile1 = objFSO.OpenTextFile("Abaqus����������s_��~���@.txt", 2, True)
objFile1.WriteLine "***�X�N���v�g�̒�~���@***"
objFile1.WriteLine " ���̃t�@�C���uAbaqus����������s_��~���@.txt�v���폜����.(5�b���x�Œ�~)"
objFile1.WriteLine " "
objFile1.WriteLine "***�X�N���v�g�̎g�����i�v�Z���s�j***"
objFile1.WriteLine " 1. �X�N���v�g�t�@�C����C�ӂ̃t�H���_�[�ɃR�s�[����."
objFile1.WriteLine " �t�@�C�����uAbaqus����������s_name.vbs�v"
objFile1.WriteLine " 2. �X�N���v�g�����s����."
objFile1.WriteLine " 3. �u�`.inp�v�t�@�C�������̃t�H���_�[�ɃR�s�[����."
objFile1.WriteLine " 4. �v�Z���I���܂ő҂�."
objFile1.WriteLine " 5. �v�Z���I�������uFinished_�`�v�̃t�H���_�[���Ǝ����̌l�t�H���_�[�Ɉړ�����."
objFile1.WriteLine " *** �X�N���v�g�����̗���"
objFile1.WriteLine "   �u�`.inp�v�t�@�C���������,�u_queued_�`.inp�v�Ƀt�@�C�����ύX"
objFile1.WriteLine "	 ���v�Z������҂�"
objFile1.WriteLine "	 ���u_queued_�`.inp�v�̖��O���Ɂu�`.inp�v�t�@�C����߂��Čv�Z����"
objFile1.WriteLine "	 ���v�Z���I������΁uFinished_�`�v�̃t�H���_���쐬�����ʃt�@�C�����ړ�"
objFile1.WriteLine "		...���̌J�Ԃ�"
objFile1.WriteLine "	* �u_queued_�`.inp�v�ɕύX���邱�ƂŃt�@�C����F�������������ɕ��ׂĂ��܂�."
objFile1.WriteLine " 	* Abaqus�g�[�N�����s������ƌv�Z��������Ɍv�Z�҂��ɂȂ�܂�."
objFile1.WriteLine "	* ���̃X�N���v�g�̋@�\�́C�������݂Čv�Z�������邾���Ȃ̂ŁC"
objFile1.WriteLine "	* �X�N���v�g���~���Ă�, Abaqus�̌v�Z�͌p������܂�."
objFile1.WriteLine "	* inp�t�@�C�����Ȃ���Ԃł��̃X�N���v�g�����s���Ă����ɉ����N���܂���."
objFile1.WriteLine " "
objFile1.WriteLine "***�X�N���v�g�̎g�����i�ݒ�ҁj***"
objFile1.WriteLine " �X�N���v�g���X�^�[�g�A�b�v�ɓo�^���Ă����ƁC�X�N���v�g�N���̎�Ԃ��Ȃ��܂��D"
objFile1.WriteLine " �uabaqus anasysis�v�Ōv�Z�������邽��, �ǂ̃o�[�W�����Ōv�Z����邩�́C"
objFile1.WriteLine "  ���̒[����abaqus.bat�̐ݒ�ɂ��܂�."
objFile1.WriteLine " "
objFile1.Close

Do

	If objFSO.FileExists("Abaqus����������s_��~���@.txt") = False Then
		objShell.Popup "�X�N���v�g����~���܂���", 4, "Abaqus����������s"
		WScript.Quit
	End If
	queueLoop(objFolder)
	WScript.sleep(1000)	 ' change the 500ms to 5000ms,that for Waiting for the .log to finish reading and writing status.
	finishLoop(objFolder)
	WScript.sleep(1000)	'delated the for loop and change the time to 2s

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
	'�w���(intThread)�v�Z���Ȃ�V���Ɏ��s���Ȃ�
	intI=0
	For Each objFile1 In objFolder.Files
		If Right(objFile1.Name, 4)=".log" Then 'change .lck to .log, to prevent .lck from appearing too slow, cause abaqus calculate 2 inp at the same time.
			intI=intI+1
		End If
	Next
	If intI >= intThread Then
		Exit Sub
	End If

	'���s����
	intJ=0
	For Each objFile1 In objFolder.Files
		If intJ >= intThread - intI Then
			Exit For
		End If
		If Right(objFile1.Name, 4)=".inp" and Left(objFile1.Name, 8)="_queued_" Then
			strFile3 = Right(objFile1.Name, Len(objFile1.Name) - 24)
			objFSO.MoveFile objFile1, strFile3
			objShell.Run "abaqus job=" & Replace(strFile3, ".inp", "") & " cpu=" & intCPU & " ask_delete=OFF"
			WScript.sleep(12000)
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