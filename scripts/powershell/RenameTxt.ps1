Get-ChildItem -Filter "*.txt" | ForEach-Object {
    Rename-Item $_.Name ("OLD_" + $_.Name)
}

Write-Output "Renaming complete."
