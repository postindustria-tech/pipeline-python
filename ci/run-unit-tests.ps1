param (
    [Parameter(Mandatory=$true)]
    [string]$RepoName
)

$packages = "fiftyone_pipeline_core", "fiftyone_pipeline_engines", "fiftyone_pipeline_engines_fiftyone"
./python/run-unit-tests.ps1 -RepoName $RepoName -Packages $packages

exit $LASTEXITCODE
