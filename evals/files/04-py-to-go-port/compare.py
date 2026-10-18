#!/usr/bin/env python3
"""Differential check: run a command on every fixture and compare stdout with the Python reference.

Usage: python3 compare.py "go run ./stats_go"      (or any command reading JSON on stdin)
Prints N inputs / M differences and exits non-zero when any output differs.
"""
import glob
import os
import shlex
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
cmd = shlex.split(sys.argv[1]) if len(sys.argv) > 1 else [sys.executable, os.path.join(here, "stats.py")]
diffs = 0
cases = sorted(p for p in glob.glob(os.path.join(here, "fixtures", "case*.json")))
for case in cases:
    with open(case, "rb") as f:
        got = subprocess.run(cmd, stdin=f, capture_output=True).stdout.decode().rstrip("\n")
    want = open(case.replace(".json", ".expected.txt")).read().rstrip("\n")
    if got != want:
        diffs += 1
        print(f"DIFF {os.path.basename(case)}\n  want: {want}\n  got:  {got}")
print(f"{len(cases)} inputs / {diffs} differences")
sys.exit(1 if diffs else 0)
