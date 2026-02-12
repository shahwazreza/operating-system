$LogFile = "server.log"

@"
Server started successfully
Error: Connection failed
User logged in
Error: Disk not found
Error: Timeout occurred
"@ | Out-File $LogFile

$Count = (Select-String -Path $LogFile -Pattern "Error").Count
Write-Output "Number of lines containing 'Error': $Count"
