#!/usr/bin/env python3
import subprocess

try:
    cm = int(input("How many commits you want? "))
except ValueError:
    print("Invalid input. Proceeding with default 100 commits")
    cm = 100

for i in range(cm):
    subprocess.run(
        [f'echo "{i}" >> gitout && git add . && git commit -m "Test commit {i}"'],
        shell=True,
        capture_output=True,
        check=False,
    )
    subprocess.run(["rm gitout"], shell=True, check=False)
