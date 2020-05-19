# -*- mode: python ; coding: utf-8 -*-
import sys, os, shutil

working_dir_files = [
                ('static/config', 'static/config'),
                ]

print('ADDED FILES: (will show up in sys._MEIPASS)')
print(working_dir_files)
print('Copying files to the dist folder')

print(os.getcwd())
for tup in working_dir_files:
        print(tup)
        to_path = os.path.join(DISTPATH, tup[1])
        if os.path.exists(to_path):
                if os.path.isdir(to_path):
                        shutil.rmtree(to_path)
                else:
                        os.remove(to_path)
        if os.path.isdir(tup[0]):
                shutil.copytree(tup[0], to_path )
        else:
                shutil.copyfile(tup[0], to_path )

block_cipher = None

a = Analysis(['Main.py'],
             pathex=['/home/ivan/PycharmProjects/MinersArchers/MinersArchers'],
             binaries=[],
             datas=[('/home/ivan/PycharmProjects/MinersArchers/MinersArchers/static/res', 'static/res')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MinersArchers',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
