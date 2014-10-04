#!/usr/bin/env python2 -OO
import argparse
import imp
import marshal
from modulefinder import ModuleFinder
import os
import sys
import zipfile


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory in which the build files were gathered.')
parser.add_argument('--main-module', default='toontown.toonbase.ClientStart',
                    help='The module to import at the start of the game.')
parser.add_argument('--output', default='GameData.zip',
                    help="The built file's name.")
args = parser.parse_args()

print 'Building the client...'

mf = ModuleFinder(path=(sys.path + [os.path.realpath(args.build_dir)]))
mf.import_hook(args.main_module)

modules = {'__main__': (False, compile('import ' + args.main_module, '__main__', 'exec'))}
for modname, mod in mf.modules.items():
    modfile = mod.__file__
    if (modfile is None) or (not modfile.endswith('.py')):
        continue
    isPackage = modfile.endswith('__init__.py')
    with open(modfile, 'r') as f:
        code = compile(f.read(), modname, 'exec')
    modules[modname] = (isPackage, code)

with zipfile.ZipFile(os.path.join(args.build_dir, args.output), 'w') as f:
    for modname, (isPackage, code) in modules.items():
        data = imp.get_magic() + ('\x00'*4) + marshal.dumps(code)
        filename = modname.replace('.', '/')
        if isPackage:
            filename += '/__init__'
        f.writestr(filename + '.pyo', data)

print 'Done building the client.'
