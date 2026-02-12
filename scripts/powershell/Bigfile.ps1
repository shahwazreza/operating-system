param (
    [string]$File
)

$Limit = 1048576  # 1MB

if (-not $File) {
    Write-Output "Usage: .\BigFile.ps1 filename"
    exit
}

if (-not (Test-Path $File)) {
    Write-Output "File does not exist."
    exit
}

$Size = (Get-Item $File).Length

if ($Size -gt $Limit) {
    Write-Output "Warning: File is too large"
}
else {
    Write-Output "File size is within limits."
}
