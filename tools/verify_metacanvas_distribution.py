#!/usr/bin/env python3
"""Check a pinned MetaCanvas standalone release against an optional MAIOS site checkout.

This checks bytes, provenance and baseline structural invariants. It does NOT
replace browser interaction, human usability, accessibility or live-site checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPT_RE = re.compile(r'<script\b(?P<attrs>[^>]*)>(?P<body>[\s\S]*?)</script\s*>', re.I)
CCM_RE = re.compile(r'<script\s+id=["\x27]ccm-data["\x27]\s+type=["\x27]application/json["\x27]\s*>([\s\S]*?)</script\s*>', re.I)


def inspect_html(raw: bytes, title: str, scene_count: int, node: str | None) -> list[str]:
    errors: list[str] = []
    try:
        html = raw.decode('utf-8')
    except UnicodeDecodeError:
        return [f'{title}: not UTF-8']
    if '<!doctype html>' not in html[:200].lower():
        errors.append(f'{title}: no HTML doctype')
    if 'SPDX-License-Identifier: MPL-2.0' not in html:
        errors.append(f'{title}: MPL-2.0 notice absent')
    data = CCM_RE.search(html)
    if not data:
        return errors + [f'{title}: missing ccm-data']
    try:
        model = json.loads(data.group(1))
        scenes = model['scenes']
        if model.get('schema') != 'ccm.document.v1':
            errors.append(f'{title}: incompatible document schema')
        if not isinstance(scenes, list) or len(scenes) != scene_count:
            errors.append(f'{title}: scene count differs from release manifest')
        scene_ids = [s['id'] for s in scenes]
        if len(set(scene_ids)) != len(scene_ids):
            errors.append(f'{title}: duplicate scene IDs')
        for scene in scenes:
            ids = [e['id'] for e in scene.get('elements', [])]
            if len(set(ids)) != len(ids):
                errors.append(f'{title}: duplicate element IDs in {scene["id"]}')
            ids = set(ids)
            for link in scene.get('links', []):
                if link.get('from') not in ids or link.get('to') not in ids:
                    errors.append(f'{title}: dangling link in {scene["id"]}')
    except (ValueError, KeyError, TypeError) as exc:
        errors.append(f'{title}: malformed ccm-data: {exc}')
    if node:
        with tempfile.TemporaryDirectory(prefix='metacanvas-release-') as tmp:
            scripts = list(SCRIPT_RE.finditer(html))
            for i, match in enumerate(scripts):
                attrs = match.group('attrs')
                if re.search(r'\bsrc\s*=', attrs, re.I):
                    errors.append(f'{title}: external script is not a standalone artifact')
                    continue
                if re.search(r'\btype\s*=\s*["\x27](?:application/json|application/ld\+json)["\x27]', attrs, re.I):
                    continue
                suffix = '.mjs' if re.search(r'\btype\s*=\s*["\x27]module["\x27]', attrs, re.I) else '.js'
                script_path = Path(tmp) / f'inline-{i}{suffix}'
                script_path.write_text(match.group('body'), encoding='utf-8')
                result = subprocess.run([node, '--check', str(script_path)], text=True, capture_output=True)
                if result.returncode:
                    errors.append(f'{title}: inline script {i} invalid: {result.stderr.strip()[:250]}')
    return errors


def verify(manifest: dict, product: Path, site: Path | None, node: str | None) -> list[str]:
    problems = []
    for row in manifest['artifacts']:
        label = row['name']
        source = product / row['source']
        if not source.is_file():
            problems.append(f'{label}: source missing: {source}')
            continue
        data = source.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != row['sha256']:
            problems.append(f'{label}: source SHA-256 drift: {digest}')
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
        if blob != row['git_blob']:
            problems.append(f'{label}: source Git blob drift: {blob}')
        problems.extend(inspect_html(data, label, row['scenes'], node))
        if site:
            target = site / row['site_asset']
            if not target.is_file():
                problems.append(f'{label}: site distribution missing: {target}')
            elif target.read_bytes() != data:
                problems.append(f'{label}: site download does not match product source')
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', type=Path, default=Path(__file__).resolve().parents[1], help='K-UX-AI repository root')
    parser.add_argument('--site', type=Path, help='maios_it repository root, optional')
    parser.add_argument('--manifest', type=Path, help='release manifest JSON, defaults beside the MetaCanvas source files')
    parser.add_argument('--skip-node', action='store_true', help='skip Node syntax checks when Node is unavailable')
    args = parser.parse_args()
    manifest_path = args.manifest or (args.product / 'examples/collaborative-communication-medium/distribution-manifest.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    node = None if args.skip_node else shutil.which('node')
    if not node and not args.skip_node:
        print('FAIL: Node unavailable; install Node or pass --skip-node (reduced evidence)', file=sys.stderr)
        return 2
    problems = verify(manifest, args.product, args.site, node)
    if problems:
        for issue in problems:
            print('FAIL:', issue)
        print(f'Failed: {len(problems)} check(s); no publication authorized by this script.')
        return 1
    print(f'PASS: {len(manifest["artifacts"])} artifacts have pinned identities, structural model checks and inline JS syntax' + ('; site copies match.' if args.site else '; site comparison not requested.'))
    print('Not checked: browser behavior, accessibility, real file:// storage, privacy of user-entered content, or live deployment.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
