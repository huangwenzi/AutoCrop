import time

import sys
# 避免递归达到1000上限
sys.setrecursionlimit(90000000)

def run(idx):
    idx += 1
    print(idx)
    if idx >= 100000:
        return idx
    return run(idx)

run(1)