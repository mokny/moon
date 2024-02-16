import sys
import os
import shutil
import mokkalib

print("Params:")
print(sys.argv)
if len(sys.argv) > 1:
    if sys.argv[1] == 'setup':
        shutil.copytree('custom', sys.argv[2])
        mokkalib.setOption('root', sys.argv[2])
        mokkalib.setOption('httpdocs', sys.argv[2] + '/www')
        mokkalib.setOption('db_filename', sys.argv[2] + '/main.db')
        print("Setup complete.")
        mokkalib.exit()
        sys.exit()