param(
    [string]$SandboxRoot = "llm_sandbox",
    [string]$PolicyFile = "llm_sandbox\\sandbox_policy.json",
    [string]$WorkingDirectory = ".",
    [Parameter(Mandatory = $true)]
    [string]$Executable,
    [string]$Arguments = ""
)

$ErrorActionPreference = "Stop"

function Resolve-InsidePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BasePath,
        [Parameter(Mandatory = $true)]
        [string]$ChildPath
    )

    return [System.IO.Path]::GetFullPath((Join-Path $BasePath $ChildPath))
}

$rootPath = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sandboxPath = Resolve-InsidePath -BasePath $rootPath -ChildPath $SandboxRoot
$policyPath = Resolve-InsidePath -BasePath $rootPath -ChildPath $PolicyFile

if (-not (Test-Path $policyPath)) {
    throw "Policy file not found: $policyPath"
}

$policy = Get-Content $policyPath -Raw | ConvertFrom-Json
$workspaceRoot = Resolve-InsidePath -BasePath $rootPath -ChildPath $policy.workspace_directory
$logRoot = Resolve-InsidePath -BasePath $rootPath -ChildPath $policy.log_directory
$targetWorkingDirectory = Resolve-InsidePath -BasePath $workspaceRoot -ChildPath $WorkingDirectory

if (-not (Test-Path $sandboxPath)) {
    throw "Sandbox root not found: $sandboxPath"
}

if (-not $targetWorkingDirectory.StartsWith($workspaceRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Working directory escapes the sandbox workspace: $targetWorkingDirectory"
}

if (-not (Test-Path $targetWorkingDirectory)) {
    New-Item -ItemType Directory -Path $targetWorkingDirectory -Force | Out-Null
}

$entryName = [System.IO.Path]::GetFileNameWithoutExtension($Executable)

foreach ($blocked in $policy.blocked_commands) {
    if ($entryName.Equals($blocked, [System.StringComparison]::OrdinalIgnoreCase) -or
        $Executable.Equals($blocked, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Blocked command by policy: $Executable"
    }
}

$inspectionFields = @($Executable, $Arguments)
foreach ($field in $inspectionFields) {
    foreach ($token in $policy.blocked_tokens) {
        if ($field.Contains($token)) {
            throw "Blocked token '$token' detected in sandbox command."
        }
    }
}

if (-not (Test-Path $logRoot)) {
    New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$logPath = Join-Path $logRoot "command-$timestamp.log"

"[$(Get-Date -Format s)] cwd=$targetWorkingDirectory" | Set-Content -Path $logPath -Encoding ascii
"[$(Get-Date -Format s)] exe=$Executable" | Add-Content -Path $logPath -Encoding ascii
"[$(Get-Date -Format s)] args=$Arguments" | Add-Content -Path $logPath -Encoding ascii

$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = $Executable
$processInfo.Arguments = $Arguments
$processInfo.WorkingDirectory = $targetWorkingDirectory
$processInfo.UseShellExecute = $false
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $processInfo

$null = $process.Start()
$stdout = $process.StandardOutput.ReadToEnd()
$stderr = $process.StandardError.ReadToEnd()
$process.WaitForExit()

if ($stdout) {
    $stdout.TrimEnd() | Tee-Object -FilePath $logPath -Append
}

if ($stderr) {
    $stderr.TrimEnd() | Tee-Object -FilePath $logPath -Append | Write-Error
}

exit $process.ExitCode
