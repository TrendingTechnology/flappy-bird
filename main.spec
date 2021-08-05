# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['C:\\Users\\thuongton999\\OneDrive\\Desktop\\flappyBird'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('FlappyBirdRegular.ttf','C:\\Users\\thuongton999\\OneDrive\\Desktop\\flappyBird\\src\\font\\FlappyBirdRegular.ttf', "DATA")]
a.datas += [('background.png', 'C:\\Users\\thuongton999\\OneDrive\\Desktop\\flappyBird\\src\\images\\background.png', "DATA")]
a.datas += [('bird.png', 'C:\\Users\\thuongton999\\OneDrive\\Desktop\\flappyBird\\src\\images\\bird.png', "DATA")]
a.datas += [('column.png', 'C:\\Users\\thuongton999\\OneDrive\\Desktop\\flappyBird\\src\\images\\column.png', "DATA")]
a.datas += [('start_button.png', 'C:\\Users\\thuongton999\\OneDrive\\Desktop\\flappyBird\\src\\images\\start_button.png', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='FlappyBird',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , version='src\\version.txt', icon='src\\images\\favicon.ico')
