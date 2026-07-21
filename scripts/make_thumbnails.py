#!/usr/bin/env python3
"""
make_thumbnails.py — optional image optimizer.

Your source PNGs are already small (30-75 KB), so this is not required. It is
here for when full-resolution originals get added: it writes web-optimized
copies capped at a max dimension so pages stay lightweight. By default it runs
in --dry-run mode and changes nothing.

    python scripts/make_thumbnails.py --apply --max-dim 1200

Requires: pillow  (pip install -r requirements.txt)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
CLASSES_DIR = REPO_ROOT / "classes"
IMAGE_EXTS = {".png", ".jpg", ".jpeg"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--max-dim", type=int, default=1400, help="max width/height in px")
    args = ap.parse_args()

    changed = 0
    for img_path in CLASSES_DIR.rglob("*"):
        if img_path.suffix.lower() not in IMAGE_EXTS or not img_path.is_file():
            continue
        with Image.open(img_path) as im:
            w, h = im.size
            if max(w, h) <= args.max_dim:
                continue
            changed += 1
            print(f"{'resize' if args.apply else 'would resize'}: "
                  f"{img_path.relative_to(REPO_ROOT)} ({w}x{h})")
            if args.apply:
                im.thumbnail((args.max_dim, args.max_dim))
                im.save(img_path)
    print(f"{changed} image(s) {'resized' if args.apply else 'would be resized'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
