Param(
    [int]$Port = 8000
)

$backendDir = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
Set-Location $backendDir

if (-Not (Test-Path .venv)) {
    Write-Host "Creating virtual environment .venv..."
    python -m venv .venv
}

$activate = Join-Path .venv\Scripts Activate.ps1
if (Test-Path $activate) {
    Write-Host "Activating .venv..."
    . .venv\Scripts\Activate.ps1
} else {
    Write-Host "Activation script not found - continuing using .venv\\python.exe directly"
}

Write-Host "Installing/ensuring dependencies (fast if already installed)..."
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Starting uvicorn on port $Port (app.main:app)"
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port $Port
