param(
    [string]$Port = "8080"
)

Set-Location $PSScriptRoot\server
Write-Host "Starting lab2 at http://localhost:$Port/lab2/"
Write-Host "Stop server: Ctrl+C"
mvn "-Djetty.http.port=$Port" jetty:run
