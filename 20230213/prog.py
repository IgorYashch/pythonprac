import glob
import sys
import zlib
import os
from os.path import basename, dirname
SHIFT = "  "

def get_branches():
    # можно убрать .. при необходимости
    return [branch for branch in glob.iglob("../.git/refs/heads/*")]


def get_commits(path, commit_id):
    for store in glob.iglob(path):
        id = basename(dirname(store)) + basename(store)

        with open(store, "rb") as f:
            obj = zlib.decompress(f.read())
            header, _, body = obj.partition(b'\x00')
            kind, size = header.split()

        if kind == b'commit' and id == commit_id:
            out = body.decode().replace('\n', '\n' + SHIFT)
            print(f"{SHIFT}{out}")

branches = get_branches()

if len(sys.argv) == 1:
    print(*(basename(b) for b in branches), sep='\n')
else:
    branch = sys.argv[1]

    if branch not in (basename(b) for b in branches):
        raise ValueError('There no such branch')

    branch_path = os.path.join(dirname(branches[0]), branch)
    my_branch_commit_id = open(branch_path, "rb").read().rstrip().decode()
    # print(my_branch_commit_id)

    get_commits("../.git/objects/??/*", my_branch_commit_id)

