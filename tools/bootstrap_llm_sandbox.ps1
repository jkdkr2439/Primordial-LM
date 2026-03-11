param(
    [string]$SandboxRoot = "llm_sandbox"
)

$ErrorActionPreference = "Stop"

$rootPath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sandboxPath = Join-Path $rootPath $SandboxRoot
$workspacePath = Join-Path $sandboxPath "workspace"
$memoryPath = Join-Path $sandboxPath "memory"
$logsPath = Join-Path $sandboxPath "logs"
$runtimePath = Join-Path $sandboxPath "runtime"
$venvPath = Join-Path $runtimePath ".venv"

foreach ($path in @($sandboxPath, $workspacePath, $memoryPath, $logsPath, $runtimePath)) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
    }
}

$readmeStub = Join-Path $workspacePath "README.md"
if (-not (Test-Path $readmeStub)) {
    @"
# Sandbox Workspace

This is the editable project area for your local coding model.
"@ | Set-Content -Path $readmeStub -Encoding ascii
}

$memoryStub = Join-Path $memoryPath "learning_log.md"
if (-not (Test-Path $memoryStub)) {
    @"
# Learning Log

- Record what the model tried.
- Keep short notes that may help future tasks.
"@ | Set-Content -Path $memoryStub -Encoding ascii
}

$pythonCommands = @("python", "py")
$pythonCommand = $null
foreach ($candidate in $pythonCommands) {
    try {
        $resolved = Get-Command $candidate -ErrorAction Stop
        $pythonCommand = $resolved.Name
        break
    } catch {
    }
}

if ($pythonCommand) {
    if (-not (Test-Path $venvPath)) {
        & $pythonCommand -m venv $venvPath
    }
    Write-Host "[sandbox] Virtual environment ready at $venvPath"
} else {
    Write-Warning "[sandbox] Python was not found. Directory structure is ready, but runtime\\.venv was not created."
}

Write-Host "[sandbox] Root: $sandboxPath"
Write-Host "[sandbox] Workspace: $workspacePath"
Write-Host "[sandbox] Memory: $memoryPath"
Write-Host "[sandbox] Logs: $logsPath"
