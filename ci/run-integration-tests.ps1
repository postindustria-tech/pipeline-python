param (
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    [Parameter(Mandatory=$true)]
    [Hashtable]$Keys
)

$packages = , "fiftyone_pipeline_cloudrequestengine"
./python/run-integration-tests.ps1 -RepoName $RepoName -Packages $packages -Keys $Keys

exit $LASTEXITCODE
