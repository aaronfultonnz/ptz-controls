# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['controls.py'],
             pathex=['C:\\Users\\Aaron\\PycharmProjects\\ptz-controls'],
             binaries=[],
             datas=[('assets', 'assets'), ('venv\\Lib\\site-packages\\wsdl', 'wsdl')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Camera Controller',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='assets\\favicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Camera Controller')
