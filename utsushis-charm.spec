# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("media", "media"),
        ("images", "images"),
        ("data", "data"),
        ("LICENSES", "LICENSES"),
    ],
    hiddenimports=["tkinter"],
    hookspath=[],
    runtime_hooks=[],
    excludes=["pandas"],
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
    name="utsushis-charm",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon="media/icon.ico",
)
