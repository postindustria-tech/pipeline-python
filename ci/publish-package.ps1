param (
    [Parameter(Mandatory=$true)]
    [Hashtable]$Keys,
    [bool]$DryRun = $False
)

$env:TWINE_REPOSITORY = "testpypi"

./python/publish-package-pypi.ps1 -Keys $Keys -DryRun $DryRun

exit $LASTEXITCODE
