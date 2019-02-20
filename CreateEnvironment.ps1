$urlGit = "https://github.com/git-for-windows/git/releases/download/v2.20.1.windows.1/Git-2.20.1-64-bit.exe"
$outputGit = "$PSScriptRoot\git.exe"
$urlPython = "https://www.python.org/ftp/python/3.7.2/python-3.7.2-amd64.exe"
$outputPy = "$PSScriptRoot\python37.exe"
if(-not(Test-Path -Path git.exe)) {
Write-Host "Downloading Git for Windows..."
Invoke-WebRequest -Uri $urlGit -OutFile $outputGit
}
if(-not(Test-Path -Path python37.exe)) {
Write-Host "Downloading Python 3.7.2..."
Invoke-WebRequest -Uri $urlPython -OutFile $outputPy
}
Write-Host "Installing Git for Windows..."
$gitPath = "git.exe"
Start-Process -FilePath $gitPath -ArgumentList ('/VERYSILENT','/NORESTART','/NOCANCEL','/SP-','/CLOSEAPPLICATIONS', '/RESTARTAPPLICATIONS', '/COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"')
Write-Host "Installing Python 3.7.2..."
$pyPath = "python37.exe"
Start-Process -FilePath $pyPath -ArgumentList ('/quiet','/InstallAllUsers=1', '/PrependPath=1', '/AssociateFiles=1')
Write-Host "Adding Python to PATH..."
$env:Path += ";C:\Users\$env:username\AppData\Local\Programs\Python\Python37\"
Write-Host "Updating pip..."
python -m pip install --upgrade pip
Write-Host "Installing tensorflow..."
python -m pip install tensorflow
Write-Host "Installing numpy..."
python -m pip install numpy
Write-Host "Installing matplotlib..."
python -m pip install matplotlib
Write-Host "Cloning Brad's TensorFlowTest Project into C:\Users\$env:username\"
Set-Location -Path C:\Users\$env:username
git clone https://github.com/soda3x/tensorFlowTest.git
Invoke-Item C:\Users\$env:username\tensorFlowTest
Write-Host "Finished :)"
Write-Host "Happy Machine Learning"
Pause
