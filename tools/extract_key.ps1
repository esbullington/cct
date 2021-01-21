
$jsonObject = Get-Content $args[0] | Out-String | ConvertFrom-Json

$toolsPath = Join-Path -Path $pwd -ChildPath 'tools'

$tempfile = Join-Path -Path $toolsPath -ChildPath "temp_rsa_key.pem"

Set-Content -Path $tempfile -Value $jsonObject.private_key.Trim()

$pythonFile = Join-Path -Path $toolsPath -ChildPath "extract_key.py"

$outFile = Join-Path -Path $toolsPath -ChildPath "temp_rsa_outfile.pem"

Start-Process -Wait -NoNewWindow -FilePath "openssl" -ArgumentList "rsa -in $tempfile -out $outFile"

$writeKeyFile = Join-Path -Path $pwd -ChildPath $args[1]
Write-Host "Writing to: $writeKeyFile"

Start-Process -Wait -NoNewWindow -FilePath "python3" -ArgumentList "$pythonFile $outFile $writeKeyFile"

Remove-Item -Path $tempfile -Force
Remove-Item -Path $outFile -Force
