# Quick start script for CVE prioritization (PowerShell)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "CrowdStrike Falcon - CVE Prioritization" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check environment variables
if (-not $env:FALCON_CLIENT_ID -or -not $env:FALCON_CLIENT_SECRET) {
    Write-Host "Error: Environment variables not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set the following environment variables:"
    Write-Host '  $env:FALCON_CLIENT_ID="your_client_id"'
    Write-Host '  $env:FALCON_CLIENT_SECRET="your_client_secret"'
    Write-Host ""
    exit 1
}

Write-Host "✓ Credentials found" -ForegroundColor Green
Write-Host ""

# Check Python dependencies
try {
    python -c "import falconpy" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw
    }
} catch {
    Write-Host "Warning: falconpy not installed" -ForegroundColor Yellow
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
}

# Create output directory
New-Item -ItemType Directory -Force -Path "reports" | Out-Null
Write-Host "✓ Output directory ready: .\reports" -ForegroundColor Green
Write-Host ""

# Menu
Write-Host "Select prioritization mode:"
Write-Host ""
Write-Host "  1) Top 20 Critical/High CVE (Quick Daily Triage)"
Write-Host "  2) All CVE with CVSS >= 7.0 (Weekly Review)"
Write-Host "  3) Active Exploitation Only (Urgent Response)"
Write-Host "  4) All vulnerabilities (Full Monthly Report)"
Write-Host "  5) Custom filter"
Write-Host ""
$choice = Read-Host "Enter choice [1-5]"

$timestamp = Get-Date -Format "yyyyMMdd"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Running: Top 20 Critical/High CVE" -ForegroundColor Yellow
        python scripts/prioritize_vulnerabilities.py `
            --filter "cve.severity:['CRITICAL','HIGH']" `
            --top 20 `
            --output-dir ./reports `
            --output-prefix "daily_triage_$timestamp" `
            --verbose
    }
    "2" {
        Write-Host ""
        Write-Host "Running: All CVE with CVSS >= 7.0" -ForegroundColor Yellow
        python scripts/prioritize_vulnerabilities.py `
            --min-score 7.0 `
            --output-dir ./reports `
            --output-prefix "weekly_review_$timestamp" `
            --verbose
    }
    "3" {
        Write-Host ""
        Write-Host "Running: Active Exploitation Only" -ForegroundColor Yellow
        python scripts/prioritize_vulnerabilities.py `
            --filter "cve.exploit_status:>=3" `
            --output-dir ./reports `
            --output-prefix "active_exploitation_$timestamp" `
            --verbose
    }
    "4" {
        Write-Host ""
        Write-Host "Running: Full vulnerability scan" -ForegroundColor Yellow
        python scripts/prioritize_vulnerabilities.py `
            --output-dir ./reports `
            --output-prefix "full_report_$timestamp" `
            --verbose
    }
    "5" {
        Write-Host ""
        $customFilter = Read-Host "Enter custom FQL filter"
        $minScore = Read-Host "Enter minimum CVSS score [0.0]"
        if ([string]::IsNullOrWhiteSpace($minScore)) { $minScore = "0.0" }

        Write-Host ""
        Write-Host "Running: Custom filter" -ForegroundColor Yellow
        $customTimestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        python scripts/prioritize_vulnerabilities.py `
            --filter "$customFilter" `
            --min-score $minScore `
            --output-dir ./reports `
            --output-prefix "custom_$customTimestamp" `
            --verbose
    }
    default {
        Write-Host "Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Prioritization complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Reports saved in: .\reports"
Write-Host ""
Get-ChildItem -Path ".\reports\*" -Include *.csv,*.json,*.xlsx | Sort-Object LastWriteTime -Descending | Select-Object -First 3 | Format-Table Name, Length, LastWriteTime
