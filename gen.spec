# -*- mode: python -*-

block_cipher = None

import sys
sys.setrecursionlimit(10000)


a = Analysis(['gen.py'],
             pathex=['D:\\Projects\\SSUGenerators'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='generators',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
