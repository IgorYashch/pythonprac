import glob
import sys
import os
import zlib
from os.path import basename, dirname

REPO_PATH = "."
HEADS_PATHS = ".git/refs/heads/*"
OBJECTS_PATHS = ".git/objects/??/*"


# Task 1
def get_branches(repo_path):
    paths = os.path.join(repo_path, HEADS_PATHS)
    return [branch for branch in glob.iglob(paths)]


def decode_commit(path):
    with open(path, "rb") as f:
        file = zlib.decompress(f.read())
        header, _, body = file.partition(b"\x00")
        return body.decode()


# Task 2
def get_commit_body(repo_path, commit_id):
    commit_path = None
    paths = os.path.join(repo_path, OBJECTS_PATHS)

    for store in glob.iglob(paths):
        id = basename(dirname(store)) + basename(store)

        if id == commit_id:
            body = decode_commit(store)
            break

    return body


def main():
    branches_paths = get_branches(REPO_PATH)
    branches_names = [basename(b) for b in branches_paths]

    if len(sys.argv) == 1:
        print(*branches_names, sep="\n")
    else:
        branch = sys.argv[1]
        if branch not in branches_names:
            raise ValueError("There is no such branch")

        branch_path = os.path.join(REPO_PATH, ".git/refs/heads", branch)
        last_commit_id = open(branch_path, "rb").read().rstrip().decode()

        # # Task 2
        commit_body = get_commit_body(REPO_PATH, last_commit_id)
        print(commit_body)


if __name__ == "__main__":
    main()