# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('TradeSettings.csv', '.'), ('FyersCredentials.csv', '.'), ('FyresIntegration.py', '.')]
binaries = []
hiddenimports = ['pandas', 'polars', 'polars_talib', 'fyers_apiv3', 'fyers_apiv3.FyersWebsocket', 'fyers_apiv3.fyersModel', 'pyotp', 'requests', 'pytz', 'urllib3', 'json', 'time', 'traceback', 'sys', 'datetime', 'math', 'warnings', 'os', 'webbrowser', 'base64', 'urllib.parse', 'configparser']
tmp_ret = collect_all('fyers_apiv3')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('polars')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pandas')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
