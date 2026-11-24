#!/usr/bin/env python3
"""Exercise all five real MetaCanvas integrity candidates using existing tests."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_metacanvas_integrity_candidates import build, EXAMPLES
from build_studio21_keyboard_section_move import build as keyboard
from build_studio21_public_projection import build as privacy_build, SOURCE_BLOBS


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


privacy = load("integrity_privacy", "metaeditor-studio21-privacy.browser.py")
rel = privacy.rel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", default=None)
    parser.add_argument("--chromium", default=None)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    names = build(args.output_root)
    originals = {p.name: (EXAMPLES / p.name).read_bytes() for p in names}
    # Prove exact continuity with the earlier two-carrier integrity build.
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        keyboard(EXAMPLES, tmp / "keyboard")
        privacy_build(tmp / "keyboard", tmp / "privacy")
        for name in SOURCE_BLOBS:
            assert (args.output_root / name).read_bytes() == (tmp / "privacy" / name).read_bytes(), name
        second = build(tmp / "second")
        for path in second:
            assert path.read_bytes() == (args.output_root / path.name).read_bytes(), path.name
        assert (tmp / "second/integrity-receipt.json").read_bytes() == (args.output_root / "integrity-receipt.json").read_bytes()
        # Refuse a changed source before writing any candidate.
        drift = tmp / "drift"
        drift.mkdir()
        for name, raw in originals.items():
            (drift / name).write_bytes(raw + (b" " if name == names[-1].name else b""))
        rejected = tmp / "rejected"
        try:
            build(rejected, drift)
        except ValueError as exc:
            assert "source drift" in str(exc)
        else:
            raise AssertionError("Accepted changed source")
        assert not rejected.exists()
    config = {"headless": True, "args": ["--no-sandbox"]}
    if args.channel:
        config["channel"] = args.channel
    if args.chromium:
        config["executable_path"] = args.chromium
    move_js = rel.MOVE.read_text(encoding="utf-8")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**config)
        try:
            for path in names:
                original = path.read_text(encoding="utf-8")
                private_html, private_model = privacy.fixture(original)
                move_html, _ = rel.fixture_html(original)
                for width in (1440, 390):
                    privacy.inspect(browser, path.name, width, private_html, private_model, False)
                    rel.observe(browser, path.name, width, move_html, move_js)
        finally:
            browser.close()
    for name, raw in originals.items():
        assert (EXAMPLES / name).read_bytes() == raw, name
    print("PASS: all five carriers, deterministic build, Studio21 parity, drift refusal, privacy and movement")


if __name__ == "__main__":
    main()
