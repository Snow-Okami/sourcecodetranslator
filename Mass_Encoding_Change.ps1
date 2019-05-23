$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding($False)
$source = "Input_Encodes"
$destination = "Output_Encodes"

foreach ($i in Get-ChildItem -Recurse -Force) {
    if ($i.PSIsContainer) {
        continue
    }

    $path = $i.DirectoryName -replace $source, $destination
    $name = $i.Fullname -replace $source, $destination

    if ( !(Test-Path $path) ) {
        New-Item -Path $path -ItemType directory
    }

    $content = get-content $i.Fullname

    if ( $content -ne $null ) {

        [System.IO.File]::WriteAllLines($name, $content, $Utf8NoBomEncoding)
    } else {
        Write-Host "No content from: $i"
    }
}
