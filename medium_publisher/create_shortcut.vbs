' VBScript to create desktop shortcut for Medium Article Publisher
' This script creates a shortcut on the user's desktop

Option Explicit

Dim objShell, objDesktop, objShortcut, strDesktop, strExePath, strWorkingDir

' Create shell object
Set objShell = CreateObject("WScript.Shell")

' Get desktop path
strDesktop = objShell.SpecialFolders("Desktop")

' Get current directory (where the executable is located)
strWorkingDir = objShell.CurrentDirectory
strExePath = strWorkingDir & "\dist\MediumArticlePublisher.exe"

' Check if executable exists
Dim objFSO
Set objFSO = CreateObject("Scripting.FileSystemObject")
If Not objFSO.FileExists(strExePath) Then
    MsgBox "Error: Executable not found at " & strExePath & vbCrLf & vbCrLf & _
           "Please build the application first using build.cmd", _
           vbCritical, "Medium Article Publisher"
    WScript.Quit 1
End If

' Create shortcut
Set objShortcut = objShell.CreateShortcut(strDesktop & "\Medium Article Publisher.lnk")
objShortcut.TargetPath = strExePath
objShortcut.WorkingDirectory = strWorkingDir & "\dist"
objShortcut.Description = "Medium Article Publisher - Automate article publishing to Medium"
objShortcut.WindowStyle = 1 ' Normal window
' objShortcut.IconLocation = strWorkingDir & "\icon.ico" ' Uncomment if icon exists
objShortcut.Save

' Confirm creation
MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & _
       "Shortcut location: " & strDesktop & "\Medium Article Publisher.lnk", _
       vbInformation, "Medium Article Publisher"

' Cleanup
Set objShortcut = Nothing
Set objFSO = Nothing
Set objShell = Nothing
