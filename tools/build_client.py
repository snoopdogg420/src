import argparse
import os
import subprocess
import pandac.PandaModules


parser = argparse.ArgumentParser()
parser.add_argument('--panda3d-dir', default='C:/Panda3D-1.9.0',
                    help='The path to the Panda3D build to use for this distribution.')
parser.add_argument('--main-module', default='infinite.base.ClientStartDist',
                    help='The path to the instantiation module.')
parser.add_argument('modules', nargs='*', default=['shared', 'infinite'],
                    help='The Toontown Infinite modules to be included in the build.')
args = parser.parse_args()

os.chdir('build')

programFilesPath = os.environ['ProgramFiles']
subprocess.Popen('"{0}\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat" x86'.format(programFilesPath), shell=True)

cmd = os.path.join(args.panda3d_dir, 'python/ppython.exe')  # ppython
cmd += ' -m direct.showutil.pfreeze'
modules = args.modules
modules.extend(['direct', 'pandac'])
for module in args.modules:
    cmd += ' -i {0}.*.*'.format(module)
cmd += ' -i {0}.*'.format('encodings')
cmd += ' -i {0}'.format('base64')
cmd += ' -i {0}'.format('site')
cmd += ' -o GameData.pyd'  # The filename of the built *.PYD.
cmd += ' {0}'.format(args.main_module)

os.system(cmd)

# TODO: Encrypt GameData.pyd.
