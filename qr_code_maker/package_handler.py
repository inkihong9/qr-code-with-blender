'''
instructions for installing additional pip packages
1. "libs" folder must exist in the same directory as this script
2. run command "python3 -m pip install <package_name> -t ./libs"
'''

import os
import sys

# this function imports all libraries stored in the "libs" folder
def import_libs():
    # Path to the "libs" folder inside the extension
    addon_dir = os.path.dirname(__file__)
    libs_dir = os.path.join(addon_dir, "libs")

    # Add to sys.path if not already there
    if libs_dir not in sys.path:
        sys.path.append(libs_dir)