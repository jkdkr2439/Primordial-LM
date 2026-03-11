# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['plm_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('primordial_llm', 'primordial_llm'), ('llm_sandbox', 'llm_sandbox')],
    hiddenimports=['rich', 'numpy', 'torch', 'transformers', 'primordial_llm', 'primordial_llm.process.context_field', 'primordial_llm.process.reproduction'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PLM_Invader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
