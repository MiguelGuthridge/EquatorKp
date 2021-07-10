"""Script for packaging into a keypirinha package
"""

import os
from zipfile import ZipFile, ZIP_DEFLATED

FILE_EXT = ".keypirinha-package"

def checkAllowed(dir: str, file: str):
    if ".git" in dir:
        return False
    if ".vscode" in dir:
        return False
    if file.endswith(FILE_EXT):
        return False
    if ".git" in file:
        return False
    if "temp" in file:
        return False
    if file == "package.py" and dir == ".":
        return False
    return True

# Thanks, https://stackoverflow.com/a/1855118/6335363

def zipdir(path: str, ziph: ZipFile):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if checkAllowed(root, file):
                ziph.write(os.path.join(root, file))

if __name__ == "__main__":
    zipf = ZipFile(f"EquatorKp{FILE_EXT}", 'w', ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
