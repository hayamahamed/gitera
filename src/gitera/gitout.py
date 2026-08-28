#!/usr/bin/env python3


import os
import shutil
import subprocess
import sys


def unsupported_platform():
    print(
        "This tool relies on POSIX terminal APIs (tty/termios) for functioning. If you are on windows, try WSL."
    )
    sys.exit(1)


if os.name != "posix":
    unsupported_platform()


import termios
import tty

hei = shutil.get_terminal_size().lines
hei = hei - 7


def run_git(args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False)


def branch_default():
    default_branch = run_git(["branch"])
    # print(default_branch.stdout.strip()[2:])
    return default_branch.stdout.strip()[2:]


def check_git_installed():
    if shutil.which("git") is None:
        print("git was not found on PATH. Please install git and try again.")
        sys.exit(1)

    result = run_git(["--version"])
    if result.returncode != 0:
        print("Found `git` on PATH, but `git --version` failed:")
        print(result.stderr.strip())
        sys.exit(1)

    return True


def check_inside_git_repo():
    result = run_git(["rev-parse", "--is-inside-work-tree"])
    if result.returncode != 0 or result.stdout.strip() != "true":
        print("Not a git repository.")
        print("(No `git init` has been run here, or you're outside a work tree.)")
        sys.exit(1)


def get_current_head_hash():
    result = run_git(["rev-parse", "--short", "HEAD"])
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def get_commits():
    """
    Return commits newest-first as a list of dicts:
        {"hash": short_hash, "subject": ..., "author": ..., "date": ...}
    """
    sep = "\x1f"  # unit separator, unlikely to appear in commit text
    fmt = f"%h{sep}%s{sep}%an{sep}%ad"
    result = run_git(["log", f"--pretty=format:{fmt}", "--date=short"])

    if result.returncode != 0:
        print("`git log` failed:")
        print(result.stderr.strip())
        sys.exit(1)

    commits = []
    for line in result.stdout.splitlines():
        parts = line.split(sep)
        if len(parts) == 4:
            h, subject, author, date = parts
            commits.append(
                {"hash": h, "subject": subject, "author": author, "date": date}
            )

    if not commits:
        print("No commits found yet — this repo has no history to browse.")
        sys.exit(1)

    return commits  # index 0 = newest / HEAD, last index = oldest


def checkout_commit(commit_hash):
    result = run_git(["checkout", commit_hash])
    return result.returncode == 0, result.stderr.strip()


UP, DOWN, ENTER, QUIT, OTHER = "UP", "DOWN", "ENTER", "QUIT", "OTHER"


def get_key():
    """Block for one keypress, decode arrow keys / Enter / quit keys."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)

        if ch == "\x1b":  # possible escape sequence (arrow keys)
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                if ch3 == "A":
                    return UP
                if ch3 == "B":
                    return DOWN
            return QUIT  # bare Esc

        if ch in ("\r", "\n"):
            return ENTER
        if ch in ("q", "Q", "\x03"):  # q or Ctrl-C
            return QUIT
        return OTHER
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


CLEAR = "\x1b[2J\x1b[H"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
REVERSE = "\x1b[41m"
DIM = "\x1b[31m"
RESET = "\x1b[0m"

MAX_ROWS = hei


def render(commits, selected, head_hash, status=""):
    n = len(commits)
    if n <= MAX_ROWS:
        start = 0
    else:
        start = max(0, min(selected - MAX_ROWS // 2, n - MAX_ROWS))
    end = min(n, start + MAX_ROWS)

    lines = [CLEAR]
    lines.append("git commit navigator — Up/Down move, Enter checkout, q quit")
    lines.append(f"({selected + 1}/{n})")
    lines.append("")

    for i in range(start, end):
        c = commits[i]
        marker = " *" if c["hash"] == head_hash else "  "
        row = f"{marker} {c['hash']}  {c['date']}  {c['subject']}"
        if i == selected:
            lines.append(f"{REVERSE}{row}{RESET}")
        else:
            lines.append(row)

    lines.append("")
    if status:
        lines.append(f"{DIM}{status}{RESET}")

    sys.stdout.write("\n".join(lines))
    sys.stdout.flush()


def main():
    check_git_installed()
    check_inside_git_repo()
    bd = branch_default()

    commits = get_commits()
    n = len(commits)
    head_hash = get_current_head_hash()

    selected = 0
    for i, c in enumerate(commits):
        if c["hash"] == head_hash:
            selected = i
            break

    status = "Use Up/Down to browse, Enter to checkout the highlighted commit."

    sys.stdout.write(HIDE_CURSOR)
    try:
        while True:
            render(commits, selected, head_hash, status)
            key = get_key()

            if key == DOWN:
                selected = (selected + 1) % n
                status = ""
            elif key == UP:
                selected = (selected - 1) % n
                status = ""
            elif key == ENTER:
                target = commits[selected]
                ok, err = checkout_commit(target["hash"])
                if ok:
                    head_hash = target["hash"]
                    status = f"Checked out at {target['hash']} — {target['subject']}"
                else:
                    status = f"checkout failed: {err}"
            elif key == QUIT:
                break
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.write("\n")
        sys.stdout.flush()

    run_git(["checkout", f"{bd}"])
    print(
        "You have been checked out to the branch you were in before running this program, gitout"
    )

    print("Goodbye.")


if __name__ == "__main__":
    main()
