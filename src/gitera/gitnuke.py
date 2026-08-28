#!/usr/bin/env python3
import subprocess


def inp():
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
        if i == 1:
            print("Started 1,2,3...")
        elif i == cm/2:
            print("Half way done...")
        elif i == cm - 1:
            print("Completed.")
        subprocess.run(["rm gitout"], shell=True, check=False)


def main():
    inp()


if __name__ == "__main__":
    main()
