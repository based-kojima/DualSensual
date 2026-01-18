# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Dual Sensual."""

import os
from pathlib import Path

block_cipher = None

# Get project root
project_root = Path(SPECPATH)

a = Analysis(
    ['src/main.py'],
    pathex=[str(project_root)],
    binaries=[
        ('hidapi.dll', '.'),
    ],
    datas=[
        ('assets', 'assets'),
        ('src/ui/styles/stylesheet.qss', 'src/ui/styles'),
    ],
    hiddenimports=[
        'pydualsense',
        'hid',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DualSensual',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/app_icon.ico',
)
