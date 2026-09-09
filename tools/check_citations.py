#!/usr/bin/env python3
"""
Fail if _data/citations.yaml is out of date with _data/sources.yaml.

sources.yaml is the hand-maintained DOI list; citations.yaml is generated from
it by tools/citations.sh and is what the Research page renders. Editing one
without regenerating the other leaves the live page showing the old list,
silently. IDs only — checking titles would mean a network call per DOI, which
is what this design keeps out of the build.

Run via ./tools/citations.sh, which uses the _cite/.venv interpreter; a bare
`python3` here is 3.7.9 and has no PyYAML.
"""

import sys
from pathlib import Path

import yaml

root = Path(__file__).resolve().parent.parent
ids = lambda p: {e["id"] for e in yaml.safe_load((root / p).read_text()) or [] if "id" in e}

want, have = ids("_data/sources.yaml"), ids("_data/citations.yaml")
if want == have:
    sys.exit(print(f"citations.yaml is in sync with sources.yaml ({len(want)} entries)."))

for i in sorted(want - have):
    print(f"  in sources.yaml but not generated:  {i}")
for i in sorted(have - want):
    print(f"  generated but no longer in sources: {i}")
sys.exit("\nerror: _data/citations.yaml is out of date. Run ./tools/citations.sh and commit both files.")
