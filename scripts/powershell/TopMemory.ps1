Get-Process |
Sort-Object -Property WorkingSet -Descending |
Select-Object -First 5 Name, Id, @{Name = "Memory(MB)"; Expression = { [math]::Round($_.WorkingSet / 1MB, 2) } }
