param (
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
	[Parameter(Mandatory=$true)]
    [string]$Version
)

$packages = "fiftyone_pipeline_core", "fiftyone_pipeline_engines", "fiftyone_pipeline_engines_fiftyone", "fiftyone_pipeline_cloudrequestengine"
./python/build-package.ps1 -RepoName $RepoName -Version $Version -Packages $packages

exit $LASTEXITCODE
