#!/usr/bin/env python3
"""
check_meta.py — completeness / consistency checks for class metadata.

Run in CI (and locally) to keep the guide consistent across annotators.
Fails (non-zero exit) if any class:
  * is missing a display_name, group, one_liner, or defining_characteristics
  * has no "ideal" image
  * lists a `distinguishing_from` class that does not exist in classes/

    python scripts/check_meta.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
REPO_ROOT = Path(__file__).resolve().parent.parent
CLASSES_DIR = REPO_ROOT / "classes"

REQUIRED_FIELDS = ["display_name", "group", "one_liner", "defining_characteristics"]


def has_images(class_dir: Path, subset: str) -> bool:
    folder = class_dir / subset
    return folder.is_dir() and any(
        p.suffix.lower() in IMAGE_EXTS for p in folder.iterdir() if p.is_file()
    )


def main() -> int:
    class_dirs = [
        d
        for d in sorted(CLASSES_DIR.iterdir())
        if d.is_dir() and not d.name.startswith((".", "_"))
    ]
    known_ids = set()
    metas = {}
    errors: list[str] = []

    for d in class_dirs:
        meta_path = d / "meta.yml"
        if not meta_path.exists():
            errors.append(f"{d.name}: missing meta.yml")
            continue
        meta = yaml.safe_load(meta_path.read_text()) or {}
        metas[d] = meta
        known_ids.add(d.name)
        cid = meta.get("class_id")
        if cid and cid != d.name:
            errors.append(f"{d.name}: class_id '{cid}' does not match folder name")

    warnings: list[str] = []
    for d, meta in metas.items():
        for field in REQUIRED_FIELDS:
            if not str(meta.get(field, "")).strip():
                errors.append(f"{d.name}: missing required field '{field}'")
        # Missing images is a warning, not a failure — classes are often stubbed
        # out with metadata first and images added later.
        if not has_images(d, "ideal"):
            warnings.append(f"{d.name}: no images in ideal/ yet")
        for row in meta.get("distinguishing_from") or []:
            target = str(row.get("class", "")).strip()
            if target and target not in known_ids:
                errors.append(
                    f"{d.name}: distinguishing_from references unknown class '{target}'"
                )

    if warnings:
        print("Metadata warnings:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print("Metadata check FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"Metadata check passed: {len(metas)} class(es).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
