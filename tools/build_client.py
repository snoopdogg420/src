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
parser.add_argument('output', default='GameData.zip',
                    help="The built file's name.")
args = parser.parse_args()

print 'Building the client...'


class Packager:
    def __init__(self, build_dir, main_module, output):
        self.build_dir = build_dir
        self.main_module = main_module
        self.output = output

        self.mf = ModuleFinder(path=(sys.path + [os.path.realpath(self.build_dir)]))

        self.modules = {}

    def load_modules(self):
        self.mf.import_hook(self.main_module)

        for modname, mod in self.mf.modules.items():
            modfile = mod.__file__
            if (modfile is None) or (not modfile.endswith('.py')):
                continue
            is_package = modfile.endswith('__init__.py')
            with open(modfile, 'r') as f:
                code = compile(f.read(), modname, 'exec')
            self.modules[modname] = (is_package, code)

        self.modules['__main__'] = \
            (False, compile('import ' + self.main_module, '__main__', 'exec'))

    def write_zip(self):
        with zipfile.ZipFile(os.path.join(self.build_dir, self.output), 'w') as f:
            for modname, (is_package, code) in self.modules.items():
                data = imp.get_magic() + ('\x00'*4) + marshal.dumps(code)
                filename = modname.replace('.', '/')
                if is_package:
                    filename += '/__init__'
                f.writestr(filename + '.pyo', data)

    def write_bin(self):
        raise NotImplementedError


packager = Packager(args.build_dir, args.main_module, args.output)
packager.load_modules()
ext = os.path.splitext(args.output)[1]
if ext == '.zip':
    packager.write_zip()
elif ext == '.bin':
    packager.write_bin()
else:
    raise NotImplementedError('Unknown package format: ' + ext)

print 'Done building the client.'
