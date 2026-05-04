param(
    [string]$Port = "8085"
)

Set-Location $PSScriptRoot\server
Write-Host "Starting lab5 at http://localhost:$Port/lab5/"
Write-Host "Stop server: Ctrl+C"
mvn "-Djetty.http.port=$Port" jetty:run
