<#
Simple build script to concatenate CSS and JS into `ollama-agents/app/static/build`.
Usage:
  .\scripts\build_static.ps1          # build bundles (no minify)
  .\scripts\build_static.ps1 -Minify  # build bundles with simple minification

Note: This is a lightweight script intended for development. It performs
basic concatenation and a very small whitespace/comment stripping when
`-Minify` is supplied. For production-grade minification use tools such as
`cssnano` and `terser`.
#>
param(
    [switch]$Minify
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$staticDir = Join-Path $repoRoot "ollama-agents\app\static"
$buildDir = Join-Path $staticDir "build"

if (-not (Test-Path $staticDir)) {
    Write-Error "Static directory not found: $staticDir"
    exit 1
}

New-Item -ItemType Directory -Force -Path $buildDir | Out-Null

# CSS bundle
$cssFiles = @(
    Join-Path $staticDir 'style.css',
    Join-Path $staticDir 'dropdown.css'
)
$cssOut = Join-Path $buildDir 'main.bundle.css'

$cssContents = @()
foreach ($f in $cssFiles) {
    if (Test-Path $f) {
        $cssContents += Get-Content -Raw -Encoding UTF8 $f
        $cssContents += "\n" # separator
    } else {
        Write-Host "Warning: CSS file missing, skipping: $f"
    }
}

$cssText = $cssContents -join "\n"
if ($Minify) {
    # Very small "minify": remove /* ... */ comments and blank lines
    $cssText = [regex]::Replace($cssText, '/\*.*?\*/', '', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    $cssText = ($cssText -split "\r?\n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }) -join "`n"
}

Set-Content -Path $cssOut -Value $cssText -Encoding UTF8 -Force
Write-Host "Wrote CSS bundle: $cssOut"

# JS bundle
$jsFiles = @(
    Join-Path $staticDir 'dropdown.js'
)
$jsOut = Join-Path $buildDir 'main.bundle.js'

$jsContents = @()
foreach ($f in $jsFiles) {
    if (Test-Path $f) {
        $jsContents += Get-Content -Raw -Encoding UTF8 $f
        $jsContents += "\n" # separator
    } else {
        Write-Host "Warning: JS file missing, skipping: $f"
    }
}

$jsText = $jsContents -join "\n"
if ($Minify) {
    # Naive JS minify: remove /* */ and // comments and collapse blank lines
    $jsText = [regex]::Replace($jsText, '/\*.*?\*/', '', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    $jsText = [regex]::Replace($jsText, '//.*?$', '', [System.Text.RegularExpressions.RegexOptions]::Multiline)
    $jsText = ($jsText -split "\r?\n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }) -join "`n"
}

Set-Content -Path $jsOut -Value $jsText -Encoding UTF8 -Force
Write-Host "Wrote JS bundle: $jsOut"

Write-Host "Build complete."
if ($Minify) { Write-Host "Note: minification performed with a simple regex-based pass. For production, use a proper minifier." }
