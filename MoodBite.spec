# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = [
    'firebase_admin',
    'google.cloud.firestore',
    'google.cloud.firestore_v1',
    'requests',
    'flask',
    'jinja2',
    'werkzeug',
]
hiddenimports += collect_submodules('firebase_admin')
hiddenimports += collect_submodules('google.cloud.firestore')
hiddenimports += collect_submodules('google.cloud.firestore_v1')
hiddenimports += collect_submodules('google.auth')
hiddenimports += collect_submodules('google.oauth2')

a = Analysis(
    ['run_moodbite.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates',          'templates'),
        ('static',             'static'),
        ('config.py',          '.'),
        ('app.py',             '.'),
        ('serviceAccountKey.json', '.'),
        ('controllers',        'controllers'),
        ('models',             'models'),
        ('services',           'services'),
    ],
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name='MoodBite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MoodBite',
)
