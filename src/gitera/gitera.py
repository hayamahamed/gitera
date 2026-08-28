#!/usr/bin/env python3
from importlib.metadata import PackageNotFoundError, version


def main():
    try:
        __version__ = version("gitera")
    except PackageNotFoundError:
        __version__ = "N/A"

    print(f"Gitera v{__version__}")
    print("Usage: gitout")
    print("Usage: got")
    print("Usage: gitnuke")
    print("Usage: gn")
    print("None of these has any sub commands so you may try all of these directly")


if __name__ == "__main__":
    main()
