"""Compile and integrate external frameworks into an iOS project.

Usage:
  kivy_libs.py build [LIBRARY]
  kivy_libs.py update [XCODEPROJ]

Arguments:
  library : The library you wish to compile. The supported libraries can be
            found in kivy-ios/recipes
  xcodeproj : The path to your .xcodeproj file that you wish to update.

Examples:
  kivy_libs.py build numpy
  kivy_libs.py update ~/Developer/numpy-ios-app/app.xcodeproj

Options:
  -h, --help

"""

from __future__ import print_function
import os, sys
from docopt import docopt

def build(library_name, kivy_dir='kivy-ios'):
    kivy_proj_dir = 'temp-{}'.format(library_name)

    # building the requested library and the kivy library
    # os.system('cd {}; ./toolchain.py build {} kivy'.format(kivy_dir,
                                                      # library_name))

    # making a (simple) kivy project (a python directory with a main.py)
    os.system('mkdir {}/{}'.format(kivy_dir, kivy_proj_dir))
    os.system('touch {}/{}/main.py'.format(kivy_dir, kivy_proj_dir))

    # making the xcodeproject to get the libraries/frameworks
    os.system('cd {}; ./toolchain.py create temp-ios-{} {}'.format(kivy_dir,
                                                library_name, kivy_proj_dir))

    # copying the libraries/frameworks to the main directory
    # the makefile will look for all files in external-libraries
    os.system('mkdir external-libraries')
    for filename in os.listdir('{}/dist/lib'.format(kivy_dir)):
        if 'python' in filename:
            continue
        os.system('cp {0}/dist/lib/{1} external-libraries/{1}'.format(kivy_dir,
                                                                  filename))

    # cleaning up, and removing the iOS project that kivy created
    os.system('cd {}; rm -rf temp-ios-{}-ios'.format(kivy_dir, library_name))
    os.system('rm -rf {}/{}/'.format(kivy_dir, kivy_proj_dir))

def update(xcodeproj, kivy_dir='kivy-ios'):
    os.system('cd {}; ./toolchain.py update {}'.format(kivy_dir, xcodeproj))

if __name__ == "__main__":
    args = docopt(__doc__)
    print("args = {}".format(args))

    if args['build']:
        build(args['LIBRARY'])
    elif args['update']:
        update(args['XCODEPROJ'])
