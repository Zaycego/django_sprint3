"""Compatibility shim for the removed stdlib `cgi` module on Python 3.13+.

Django 3.2 expects `cgi.parse_header` and `cgi.valid_boundary`. This file
implements the minimal subset used by Django so the project can run on
Python versions where `cgi` is no longer bundled.
"""

import re
from typing import Dict, Tuple

# Regex from CPython 3.11 cgi.valid_boundary implementation.
_BOUNDARY_RE = re.compile(rb"^[ -~]{0,200}[!-~]$")


def valid_boundary(boundary) -> bool:
    """Return True if the multipart boundary is syntactically valid."""
    if not boundary:
        return False
    if isinstance(boundary, str):
        boundary = boundary.encode("ascii", "replace")
    return bool(_BOUNDARY_RE.match(boundary))


def parse_header(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-Type like header into key and params dict.

    Replicates the behavior of `cgi.parse_header` from Python 3.11.
    """
    if not line:
        return "", {}
    parts = line.split(";")
    key = parts[0].strip().lower()
    pdict: Dict[str, str] = {}
    for item in parts[1:]:
        if "=" not in item:
            continue
        name, value = item.split("=", 1)
        name = name.strip().lower()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        pdict[name] = value
    return key, pdict
