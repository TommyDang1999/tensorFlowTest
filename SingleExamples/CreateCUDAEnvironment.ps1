Add-Type -AssemblyName System.IO.Compression.FileSystem

# create an unzipper
function Unzip {
    param([string]$zipfile, [string]$outpath)
    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipfile, $outpath)
}

$urlCUDA = "https://developer.nvidia.com/compute/cuda/10.0/Prod/network_installers/cuda_10.0.130_win10_network"
$outputCUDA = "$PSScriptRoot\cuda.exe"
$urlcudnn = "http://developer.download.nvidia.com/compute/redist/cudnn/v7.0.5/cudnn-9.0-windows10-x64-v7.zip"
$outputcudnn = "$PSScriptRoot\cudnn.zip"

# check if CUDA Toolkit downloaded
if(-not(Test-Path -Path $outputCUDA)) {
    Write-Host "Downloading CUDA Toolkit..."
    Invoke-WebRequest -Uri $urlCUDA -OutFile $outputCUDA
} else {
    Write-Host "CUDA Toolkit already Downloaded, Skipping download of CUDA Toolkit"
}

# check if CuDNN downloaded
if(-not(Test-Path -Path $outputcudnn)) {
    Write-Host "Downloading CuDNN..."
    Invoke-WebRequest -Uri $urlcudnn -OutFile $outputcudnn
} else {
    Write-Host "CuDNN already Downloaded, Skipping download of CuDNN"
}

# check if CUDA Toolkit installed
if(-not(Test-Path -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin\cudafe++.exe")) {
Write-Host "Installing CUDA Toolkit..."
$cudaPath = $outputCUDA
Start-Process -FilePath $cudaPath -ArgumentList ('-s compiler_8.0','-Wait','-NoNewWindow')
} else {
    Write-Host "CUDA Toolkit Found, Skipping Installation of CUDA Toolkit"
}

# check if CuDNN installed
if(-not(Test-Path -Path "C:\tools\cuda\bin\cudnn64_7.dll")) {
    $cudnnPath = "cudnn.zip"
    Write-Host "Extracting cuDNN..."
    Unzip "$cudnnPath" "C:\tools"
} else {
    Write-Host "CuDNN Found, Skipping Installation of CuDNN"
}

Write-Host "There is no reliable way to automatically add CUDA and CuDNN to PATH via Powershell"
Write-Host "Add the following directories to Path:"
Write-Host "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\bin"
Write-Host "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\extras\CUPTI\libx64"
Write-Host "C:\tools\cuda\bin"
# open environment variables window so that user may edit Path
Start-Process rundll32 sysdm.cpl,EditEnvironmentVariables
Write-Host "Script complete."
pause