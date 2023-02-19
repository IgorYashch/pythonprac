import glob
import sys
import os
from os.path import basename, dirname

REPO_PATH = "."
HEADS_PATHS = ".git/refs/heads/*"
OBJECTS_PATHS = ".git/objects/??/*"


# Task 1
def get_branches(repo_path):
    paths = os.path.join(repo_path, HEADS_PATHS)
    return [branch for branch in glob.iglob(paths)]


def main():
    branches_paths = get_branches(REPO_PATH)
    branches_names = [basename(b) for b in branches_paths]

    if len(sys.argv) == 1:
        print(*branches_names, sep="\n")
    else:
        pass


if __name__ == "__main__":
    main()