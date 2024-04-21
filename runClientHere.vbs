Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c runClient_python312.bat"
oShell.Run strArgs, 0, false