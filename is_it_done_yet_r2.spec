# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['is_it_done_yet_r2.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Eric\\AppData\\Local\\Programs\\Python\\Python313\\tcl\\tk8.6\\tkdnd2.9', 'tkdnd')],
    hiddenimports=[],
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
    name='is_it_done_yet_r2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
