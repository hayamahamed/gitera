#!/usr/bin/env python3
import subprocess

for i in range(100):
    subprocess.run(
        [f'echo "{i}" >> gitout && git add . && git commit -m "Test commit {i}"'],
        shell=True,
        capture_output=True,
        check=False,
    )
    subprocess.run(["rm gitout"], shell=True, check=False)
