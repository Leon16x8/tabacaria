Set objShell = CreateObject("WScript.Shell")
Set objShortcut = objShell.CreateShortcut(objShell.SpecialFolders("Desktop") & "\Controle de Vendas Fabio Pipas & RBShop.lnk")
objShortcut.TargetPath = objShell.ExpandEnvironmentStrings("%ProgramFiles%\Controle de Vendas Fabio Pipas & RBShop\main.exe")
objShortcut.WorkingDirectory = objShell.ExpandEnvironmentStrings("%ProgramFiles%\Controle de Vendas Fabio Pipas & RBShop")
objShortcut.IconLocation = objShell.ExpandEnvironmentStrings("%ProgramFiles%\Controle de Vendas Fabio Pipas & RBShop\imagens\logoprincipal.ico")
objShortcut.Save
