Write-Host "Starting installation..."

choco install visualstudiocode -y
choco install git -y
choco install openssl.light -y
choco install python -y

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") 

Write-Host "Pip installations..."

c:\python39\python.exe -m pip install --upgrade pip

pip install rsa
pip install esptool
pip install rshell

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") 

Write-Host "VSCode installations..."

code --install-extension VisualStudioExptTeam.vscodeintellicode
code --install-extension ms-python.vscode-pylance
