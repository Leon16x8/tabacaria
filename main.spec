# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\leona\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\PyQt5\\Qt5\\bin'],
    binaries=[],
    datas=[('imagens/logoprincipal.ico', 'imagens'), ('imagens/logoprincipal.png', 'imagens'), ('banco_de_dados/sistema_vendas.db', '.'), ('C:\\Users\\leona\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\PyQt5\\Qt5\\bin', 'PyQt5\\Qt5\\bin')],
    hiddenimports=['PyQt5.sip', 'openpyxl', 'bcrypt', 'sqlite3', 'pandas', 'PyQt5', 'shutil'],
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
    name='main',
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
    uac_admin=True,
    icon=['imagens\\logoprincipal.ico'],
)
