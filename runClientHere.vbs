Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c Client.bat"
oShell.Run strArgs, 0, false