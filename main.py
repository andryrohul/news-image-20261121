#!/usr/bin/env python3
"""Entry point for the news-image-20261121 bounty.

The front page was drawn on the build machine and ships in this
repository as entry.png. This program only copies that image to the
grader output directory, using the Python standard library alone.
It writes the same bytes on every run: no network, no randomness,
no timestamps.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
