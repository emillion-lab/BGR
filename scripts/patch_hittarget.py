#!/usr/bin/env python3
# BGR patch #3 — search box hit target (the 🔍 span swallowed the tap)
# Idempotent. Marker: BGR-PATCH-HITTARGET-v1
import sys, io

PATH = "index.html"
MARK = "BGR-PATCH-HITTARGET-v1"

# NOTE: scope to `.sb .si` only. A second, unrelated `.si` rule exists
# (section grid container) and must not be touched.
CSS = """
/* ═══ BGR-PATCH-HITTARGET-v1 ═══ */
.sb .si{pointer-events:none}
.sb{cursor:text}
.sb input{min-height:40px}
"""

def main():
    src = io.open(PATH, encoding="utf-8").read()
    if MARK in src:
        print("SKIP: " + MARK + " already applied")
        return 0
    if ".sb .si{position:absolute" not in src:
        print("FAIL: .sb .si rule not found — layout changed"); return 1
    i = src.rfind("</style>")
    if i == -1:
        print("FAIL: </style> not found"); return 1
    src = src[:i] + CSS + src[i:]
    io.open(PATH, "w", encoding="utf-8").write(src)
    print("OK: hit-target patch applied")
    return 0

sys.exit(main())
