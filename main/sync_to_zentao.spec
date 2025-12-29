# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['sync_to_zentao.py'],
    pathex=[],
    binaries=[],
    datas=[('libmirror/mstr.py', '.'), ('libmirror/mconfig.py', '.'), ('libmirror/mio.py', '.'), ('libmirror/mlogger.py', '.'), ('libmirror/mpath.py', '.'), ('libmirror/mjira/const.py', 'mjira'), ('libmirror/mjira/field.py', 'mjira'), ('libmirror/mjira/issue.py', 'mjira'), ('libmirror/mjira/http.py', 'mjira'), ('libmirror/mjira/net_sony.py', 'mjira'), ('libmirror/mzendao/*.py', 'mzendao')],
    hiddenimports=['json', 'colorama', 'jira', 'translate', 'openpyxl'],
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
    name='sync_to_zentao',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
