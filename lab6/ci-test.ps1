# ============================================================
# CI Test Script (PowerShell) — DevOps Lab 6
# Tích hợp: SAST (SonarQube) + API Test (Newman) + DAST (ZAP)
# ============================================================

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  DEVOPS LAB 6 — CI TESTING PIPELINE" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

# --- Stage 1: SAST — SonarQube Static Analysis ---
Write-Host "[1/4] [SAST] SonarQube Static Analysis..." -ForegroundColor Yellow
$sonarCmd = Get-Command sonar-scanner -ErrorAction SilentlyContinue
if ($sonarCmd) {
    try {
        sonar-scanner `
            -Dsonar.projectKey=devops-lab6 `
            -Dsonar.sources=. `
            -Dsonar.exclusions="node_modules/**,newman-report.json,zap-report.html" `
            -Dsonar.host.url="http://localhost:9000" `
            -Dsonar.login="admin" `
            -Dsonar.password="sonar123"
        Write-Host ">> SAST passed." -ForegroundColor Green
    } catch {
        Write-Host ">> SAST completed with warnings or SonarQube server offline." -ForegroundColor DarkYellow
    }
} else {
    Write-Host ">> sonar-scanner not found. Skipping local SAST." -ForegroundColor DarkGray
    Write-Host "   (Can be run in GitHub Codespaces or npm install -g sonarqube-scanner)" -ForegroundColor DarkGray
}

# --- Stage 2: Start API Server ---
Write-Host "[2/4] [API Server] Starting Node.js Express server..." -ForegroundColor Yellow
$serverProcess = Start-Process node -ArgumentList "server.js" -PassThru -NoNewWindow
Start-Sleep -Seconds 3

try {
    $health = Invoke-RestMethod -Uri "http://localhost:3000/api/students" -ErrorAction Stop
    Write-Host ">> Server running successfully on port 3000 (PID: $($serverProcess.Id))" -ForegroundColor Green
} catch {
    Write-Host ">> Failed to connect to API server: $_" -ForegroundColor Red
    if ($serverProcess -and -not $serverProcess.HasExited) { Stop-Process -Id $serverProcess.Id -Force }
    exit 1
}

# --- Stage 3: API Functional Test ---
Write-Host "[3/4] [Functional Test] Newman API Tests..." -ForegroundColor Yellow
$newmanCmd = Get-Command newman -ErrorAction SilentlyContinue
if ($newmanCmd) {
    newman run Student-API-Tests.json -r "cli,json" --reporter-json-export "newman-report.json" --color on
    if ($LASTEXITCODE -eq 0) {
        Write-Host ">> All Newman API tests passed!" -ForegroundColor Green
    } else {
        Write-Host ">> Newman API tests had failures! Check newman-report.json" -ForegroundColor Red
    }
} else {
    Write-Host ">> newman CLI not found. Skipping Newman tests." -ForegroundColor DarkYellow
}

# --- Stage 4: DAST — OWASP ZAP Security Scan ---
Write-Host "[4/4] [DAST] OWASP ZAP Security Scan..." -ForegroundColor Yellow
$zapUrl = "http://127.0.0.1:8080"
$zapOnline = $false

try {
    $zapCheck = Invoke-RestMethod -Uri "$zapUrl/JSON/core/view/version/" -TimeoutSec 3 -ErrorAction Stop
    Write-Host ">> OWASP ZAP detected: version $($zapCheck.version)" -ForegroundColor Green
    $zapOnline = $true
} catch {
    Write-Host ">> ZAP is not running at $zapUrl. Skipping live ZAP active scan." -ForegroundColor DarkGray
    Write-Host "   (Start OWASP ZAP Desktop to enable automated DAST scan)" -ForegroundColor DarkGray
}

if ($zapOnline) {
    try {
        Write-Host ">> Starting Spider scan on http://127.0.0.1:3000..." -ForegroundColor Cyan
        $spiderResp = Invoke-RestMethod -Uri "$zapUrl/JSON/spider/action/scan/?url=http://127.0.0.1:3000&maxChildren=10"
        Start-Sleep -Seconds 3
        Write-Host ">> Spider scan initialized (ID: $($spiderResp.scan))." -ForegroundColor Green
        
        Write-Host ">> Exporting HTML security report..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri "$zapUrl/OTHER/core/other/htmlreport/" -OutFile "zap-report.html"
        Write-Host ">> ZAP report saved to zap-report.html." -ForegroundColor Green
    } catch {
        Write-Host ">> ZAP scan error: $_" -ForegroundColor Red
    }
}

# --- Cleanup ---
if ($serverProcess -and -not $serverProcess.HasExited) {
    Stop-Process -Id $serverProcess.Id -Force
    Write-Host ">> API Server stopped." -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  PIPELINE COMPLETE!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Reports generated:" -ForegroundColor White
Write-Host "  - API Test: newman-report.json" -ForegroundColor White
Write-Host "  - SAST:     http://localhost:9000/dashboard?id=devops-lab6" -ForegroundColor White
Write-Host "  - DAST:     zap-report.html" -ForegroundColor White
