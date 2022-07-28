Option Explicit

Dim objShell, objFSO
Dim objFolder, objFile1, objFile2, strFile3
Dim intCPU, intThread
Dim intI, intJ, intK, strNow

intCPU=8     '�v�Z����CPU�����uintCPU=�v�̂��Ƃɔ��p�����ŏ����i1�A2�A4�A8�Ƃ��G4�����j
intThread=1  '�����Ɍv�Z����{�����uintThread=�v�̂��Ƃɔ��p�����ŏ����i1�A2�A3�Ƃ��G1�����j

Set objShell = CreateObject("WScript.Shell")
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")

Set objFolder = objFSO.GetFolder(objShell.CurrentDirectory)

Set objFile1 = objFSO.OpenTextFile("Abaqus����������s_��~���@.txt", 2, True)
objFile1.WriteLine "���X�N���v�g�̒�~���@"
objFile1.WriteLine "�@���̃t�@�C���uAbaqus����������s_��~���@.txt�v���폜����D�i5�b���x�Œ�~�j"
objFile1.WriteLine " "
objFile1.WriteLine "���X�N���v�g�̎g�����i�v�Z���s�j"
objFile1.WriteLine "�@1. �X�N���v�g�t�@�C����C�ӂ̃t�H���_�[�ɃR�s�[����D"
objFile1.WriteLine "�@�@ �t�@�C�����uAbaqus����������s_???.vbs�v"
objFile1.WriteLine "�@2. �X�N���v�g�����s����D"
objFile1.WriteLine "�@3. �u�`.inp�v�t�@�C�������̃t�H���_�[�ɃR�s�[����D"
objFile1.WriteLine "�@4. �v�Z���I���܂ő҂D"
objFile1.WriteLine "�@5. �v�Z���I�������uFinished_�`�v�̃t�H���_�[���Ǝ����̌l�t�H���_�[�Ɉړ�����D"
objFile1.WriteLine "�@�� �X�N���v�g�����̗���"
objFile1.WriteLine "�@�@  �u�`.inp�v�t�@�C��������΁C�u_queued_�`.inp�v�Ƀt�@�C�����ύX"
objFile1.WriteLine "�@�@ ���v�Z������҂�"
objFile1.WriteLine "�@�@ ���u_queued_�`.inp�v�̖��O���Ɂu�`.inp�v�t�@�C����߂��Čv�Z����"
objFile1.WriteLine "�@�@ ���v�Z���I������΁uFinished_�`�v�̃t�H���_���쐬�����ʃt�@�C�����ړ�"
objFile1.WriteLine "�@�@ �@...���̌J�Ԃ�"
objFile1.WriteLine "�@�� �u_queued_�`.inp�v�ɕύX���邱�ƂŃt�@�C����F�������������ɕ��ׂĂ��܂��D"
objFile1.WriteLine "�@�� Abaqus�g�[�N�����s������ƌv�Z��������Ɍv�Z�҂��ɂȂ�܂��D"
objFile1.WriteLine "�@�� ���̃X�N���v�g�̋@�\�́C�������݂Čv�Z�������邾���Ȃ̂ŁC"
objFile1.WriteLine "�@�@ �X�N���v�g���~���Ă��CAbaqus�̌v�Z�͌p������܂��D"
objFile1.WriteLine "�@�� inp�t�@�C�����Ȃ���Ԃł��̃X�N���v�g�����s���Ă����ɉ����N���܂���D"
objFile1.WriteLine " "
objFile1.WriteLine "���X�N���v�g�̎g�����i�ݒ�ҁj"
objFile1.WriteLine "�@�X�N���v�g���X�^�[�g�A�b�v�ɓo�^���Ă����ƁC�X�N���v�g�N���̎�Ԃ��Ȃ��܂��D"
objFile1.WriteLine "�@�uabaqus anasysis�v�Ōv�Z�������邽�߁C�ǂ̃o�[�W�����Ōv�Z����邩�́C"
objFile1.WriteLine "�@���̒[����abaqus.bat�̐ݒ�ɂ��܂��D"
objFile1.WriteLine " "
objFile1.Close

Do
	For intK = 1 to 5
		If objFSO.FileExists("Abaqus����������s_��~���@.txt") = False Then
			objShell.Popup "�X�N���v�g����~���܂���", 4, "Abaqus����������s"
			WScript.Quit
		End If
		queueLoop(objFolder)
		WScript.sleep(500)	
		finishLoop(objFolder)
		WScript.sleep(500)	
	Next
    
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
			strFile3 = objFile1.Name
			strNow = Year(Now) & right("0" & Month(Now), 2) & right("0" & Day(Now), 2) & "_" & right("0" & Hour(Now), 2) & right("0" & Minute(Now), 2) & right("0" & Second(Now), 2) 
			objFSO.CreateFolder(objFolder & "\Finished_" & strNow & "_" & Replace(objFile1.Name, ".odb", ""))

			For Each objFile2 In objFolder.Files
				If InStr(objFile2, Replace(strFile3, ".odb", "")) > 0 Then
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
		If Right(objFile1.Name, 4)=".lck" Then
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
			objShell.Run "abaqus job=" & Replace(strFile3, ".inp", "") & " cpus=" & intCPU & " gpus=1 ask_delete=OFF"
			WScript.sleep(10000)
			intJ = intJ + 1
		End If
        If intJ >= intThread - intI Then
            Exit For
		End If
	Next
End Sub