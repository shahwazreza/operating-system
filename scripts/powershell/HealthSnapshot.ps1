Write-Output "===== System Health Snapshot ====="
Write-Output "Date & Time: $(Get-Date)"
Write-Output "Hostname: $env:COMPUTERNAME"
Write-Output "Current User: $env:USERNAME"
Write-Output ""
Write-Output "Disk Usage:"

Get-PSDrive C | Select-Object `
    @{Name="Free(GB)";Expression={[math]::Round($_.Free/1GB,2)}}, `
    @{Name="Total(GB)";Expression={[math]::Round(($_.Used+$_.Free)/1GB,2)}}
