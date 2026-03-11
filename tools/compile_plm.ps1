
# PLM Standalone Compilation Tool
# Uses PyInstaller to bundle the Primordial Language Machine

$ErrorActionPreference = "Stop"

$EXE_NAME = "PLM_Invader"
$ENTRY_POINT = "plm_launcher.py"

Write-Host "--- [PLM COMPILATION START] ---" -ForegroundColor Cyan

# Check for PyInstaller
if (!(Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found in path. Trying to run via python -m..." -ForegroundColor Yellow
    $PY_INSTALLER = "python -m PyInstaller"
} else {
    $PY_INSTALLER = "pyinstaller"
}

# Define hidden imports and data files
$HIDDEN_IMPORTS = @(
    "rich",
    "numpy",
    "torch",
    "transformers",
    "primordial_llm",
    "primordial_llm.process.context_field",
    "primordial_llm.process.reproduction"
)

$IMPORT_ARGS = ""
foreach ($import in $HIDDEN_IMPORTS) {
    $IMPORT_ARGS += " --hidden-import $import"
}

# Run PyInstaller
Write-Host "Packing organs into executable..." -ForegroundColor Green
Invoke-Expression "$PY_INSTALLER --onefile --name $EXE_NAME $IMPORT_ARGS --add-data 'primordial_llm;primordial_llm' --add-data 'llm_sandbox;llm_sandbox' $ENTRY_POINT"

Write-Host "`n--- [COMPILATION COMPLETE] ---" -ForegroundColor Cyan
Write-Host "Executable can be found in the 'dist' folder as $EXE_NAME.exe" -ForegroundColor Green
