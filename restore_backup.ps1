# Restore project to April 5, 2026 backup (3 days ago)
# Target timestamp: 1775388379763 (2026-04-05 11:26:19)

$historyRoot = "C:\Users\anaso\AppData\Roaming\Code\User\History"
$projectPath = "d:\first"
$targetTimestamp = 1775388379763
$restoredCount = 0
$failedCount = 0

Write-Host "========== PROJECT RESTORATION SCRIPT ==========" -ForegroundColor Cyan
Write-Host "Target: $projectPath" -ForegroundColor Cyan
Write-Host "Restore Date: April 5, 2026 (3 days ago)" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Find all history directories
$historyDirs = Get-ChildItem -Path $historyRoot -Directory -ErrorAction SilentlyContinue

# Dictionary to store file mappings
$restoreMap = @{}

# Scan all history directories for d:\first project files
foreach ($dir in $historyDirs) {
    $entriesFile = Join-Path $dir.FullName "entries.json"
    
    if (Test-Path $entriesFile) {
        try {
            $entries = Get-Content $entriesFile -Raw | ConvertFrom-Json
            
            # Check if this directory contains d:\first files
            if ($entries.resource -match "d%3A/first") {
                $resource = $entries.resource -replace "file:///", "" -replace "%3A", ":" -replace "%20", " "
                
                # Find the latest version before or at target timestamp
                $latestEntry = $entries.entries | 
                    Where-Object { [Int64]$_.timestamp -le $targetTimestamp } | 
                    Sort-Object { [Int64]$_.timestamp } -Descending | 
                    Select-Object -First 1
                
                if ($latestEntry) {
                    $restoreMap[$resource] = @{
                        HistoryFile = Join-Path $dir.FullName $latestEntry.id
                        Timestamp = $latestEntry.timestamp
                        HistoryDir = $dir.Name
                        EntryID = $latestEntry.id
                    }
                }
            }
        }
        catch {
            # Silently skip on error
        }
    }
}

Write-Host "Found $($restoreMap.Count) files to restore" -ForegroundColor Yellow
Write-Host ""

# Restore each file
foreach ($originalPath in ($restoreMap.Keys | Sort-Object)) {
    $info = $restoreMap[$originalPath]
    $backupFile = $info.HistoryFile
    
    # Ensure the directory exists
    $dirPath = Split-Path $originalPath
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
    
    # Copy backup to original location
    if (Test-Path $backupFile) {
        try {
            Get-Content $backupFile -Raw | Set-Content -Path $originalPath -NoNewline
            Write-Host "Restored: $originalPath" -ForegroundColor Green
            $restoredCount++
        }
        catch {
            Write-Host "Failed: $originalPath" -ForegroundColor Red
            $failedCount++
        }
    }
    else {
        Write-Host "Backup not found: $backupFile" -ForegroundColor Red
        $failedCount++
    }
}

Write-Host ""
Write-Host "========== RESTORATION COMPLETE ==========" -ForegroundColor Cyan
Write-Host "Successfully restored: $restoredCount files" -ForegroundColor Green
if ($failedCount -gt 0) {
    Write-Host "Failed: $failedCount files" -ForegroundColor Red
}
Write-Host "=========================================" -ForegroundColor Cyan
