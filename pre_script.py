import subprocess
import sys
import os

# Path to the Blender Python executable
# this is for Windows, will need to adjust for other OS
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

# Upgrade pip to the latest version
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

# Install the desired package
subprocess.call([python_exe, "-m", "pip", "install", "qrcode"])