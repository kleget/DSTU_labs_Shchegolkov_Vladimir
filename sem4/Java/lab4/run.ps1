param(
    [string]$Port = "8080"
)

Set-Location $PSScriptRoot\server
Write-Host "Starting lab4 at http://localhost:$Port/lab4/"
Write-Host "Stop server: Ctrl+C"
mvn "-Djetty.http.port=$Port" jetty:run
