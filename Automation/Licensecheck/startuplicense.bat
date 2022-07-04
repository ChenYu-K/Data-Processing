@echo off 
if "%1"=="h" goto begin 
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit 
:begin 
::
start /b cmd /k "C:\Users\bridge1\anaconda3\pythonw.exe C:/Users/bridge1/Desktop/Untitled1.py"
