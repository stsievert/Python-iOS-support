"""
Usage:

    python make-kivy-library.py <library-name>

where <library-name> is a directory in kivy-ios/recipes/
"""

from __future__ import print_function
import os, sys

if __name__ == "__main__":
    if sys.argv[1] == None:
        print("Usage: python make-kivy-library.py [dir name]")
        sys.exit()

    kivy_dir = 'kivy-ios'
    library_name = sys.argv[1]
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
