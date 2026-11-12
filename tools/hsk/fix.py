"""Apply sentence fixes: python3 fix.py FILE PAIRS_FILE.
PAIRS_FILE has blocks separated by blank lines: line 1 old text, line 2 new text."""
import sys
f, pf = sys.argv[1], sys.argv[2]
s = open(f).read()
blocks = [b.split("\n") for b in open(pf).read().strip().split("\n\n")]
for b in blocks:
    old, new = b[0], b[1]
    if old not in s:
        print("MISSING:", old)
    s = s.replace(old, new)
open(f, "w").write(s)
