import glob
import sys
from os.path import basename, dirname


if len(sys.argv) == 1:
    # можно убрать .. при необходимости
    for branch in glob.iglob("../.git/refs/heads/*"):
        print(basename(branch))
else:
    pass