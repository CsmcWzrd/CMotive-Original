#!/usr/bin/env sh
set -eu
test -f release/provenance/manifest.json
python3 scripts/package_release.py --root . --out dist
