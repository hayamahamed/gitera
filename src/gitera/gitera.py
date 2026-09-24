#!/usr/bin/env python3
from importlib.metadata import PackageNotFoundError, version


def main():
    try:
        __version__ = version("gitera")
    except PackageNotFoundError:
        __version__ = "N/A"

    print(f"Gitera v{__version__}")
    print("Usage: gitout / got : view all commits of a repo in a single scrollable view with enter as checking out.")
    print("Usage: gitnuke / gne : create numerous amount of specified commits for testing purposes.")
    print("None of these has any sub commands so you may try all of these directly")


if __name__ == "__main__":
    main()
