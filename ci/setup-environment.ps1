param (
    [Parameter(Mandatory=$true)]
    [string]$LanguageVersion
)

$dependencies ="pylint", "unittest-xml-reporting", "coverage", "parameterized", "requests-mock", "flask"
./python/setup-environment.ps1 -LanguageVersion $LanguageVersion -Dependencies $dependencies

exit $LASTEXITCODE
