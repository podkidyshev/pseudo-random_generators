# -*- mode: python -*-

block_cipher = None

import sys
sys.setrecursionlimit(10000)


a = Analysis(['main.py'],
             pathex=['D:\\Projects\\SSU-Generators\\task_1\\release'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             cipher=block_cipher)

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='generators.exe',
          debug=False,
          strip=None,
          upx=False,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=False,
               name='lib')
