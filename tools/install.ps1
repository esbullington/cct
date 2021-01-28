Write-Host "Starting installation..."

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

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
pip install pylint

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") 

Write-Host "VSCode installations..."

code --install-extension VisualStudioExptTeam.vscodeintellicode
code --install-extension ms-python.vscode-pylance
