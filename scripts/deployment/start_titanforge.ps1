# start_titanforge.ps1

# Navigate to the project root directory
Push-Location $PSScriptRoot

Write-Host "Starting Docker Compose services (db, redis, backend)..."
docker-compose up -d db redis backend

Write-Host "Navigating to frontend directory and installing dependencies..."
Set-Location frontend
npm install

Write-Host "Starting frontend development server..."
npm run dev

Write-Host "TitanForge services started. Frontend accessible at http://localhost:5173 (or as indicated by npm run dev)."
