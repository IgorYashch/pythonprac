import glob
import sys
import zlib
import os
from os.path import basename, dirname
SHIFT = "  "

def get_branches():
    # можно убрать .. при необходимости
    return [branch for branch in glob.iglob("../.git/refs/heads/*")]


def print_commit(path, commit_id):
    for store in glob.iglob(path):
        id = basename(dirname(store)) + basename(store)

        with open(store, "rb") as f:
            obj = zlib.decompress(f.read())
            header, _, body = obj.partition(b'\x00')
            kind, size = header.split()

        if id == commit_id:
            out = body.decode()
            print(f"{out}")


def print_last_tree(path, commit_id):
    for store in glob.iglob(path):
        id = basename(dirname(store)) + basename(store)

        with open(store, "rb") as f:
            obj = zlib.decompress(f.read())
            header, _, body = obj.partition(b'\x00')
            kind, size = header.split()

        if kind == b'commit' and id == commit_id:
            tree_id = body.decode().split()[1]
            break

    for store in glob.iglob(path):
        id = basename(dirname(store)) + basename(store)
        if id == tree_id:
            with open(store, "rb") as f:
                obj = zlib.decompress(f.read())
                header, _, body = obj.partition(b'\x00')
                kind, size = header.split()

            tail = body
            while tail:
                treeobj, _, tail = tail.partition(b'\x00')
                tmode, tname = treeobj.split()
                num, tail = tail[:20], tail[20:]
                if tmode.decode() == '40000':
                    tmode_name = "tree"
                elif tmode.decode() == "100644":
                    tmode_name = "blob"

                print(f"{tmode_name} {num.hex()}    {tname.decode()}")
            break

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

    # print_commit("../.git/objects/??/*", my_branch_commit_id)
    print_last_tree("../.git/objects/??/*", my_branch_commit_id)
