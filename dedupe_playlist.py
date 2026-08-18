#!/usr/bin/env python3
"""
dedupe_playlist.py
Keep-last dedupe based on SoundId (keep the last occurrence of each SoundId).
Usage:
  python3 dedupe_playlist.py playlistrealshadowhall.json
This will:
 - create a backup file playlistrealshadowhall.json.bak (if not exists)
 - write deduped output to playlistrealshadowhall.json (overwrite)

IMPORTANT: Run this locally or in CI, then review the changed file before merging.
"""
import sys
import json
import os
from pathlib import Path

def dedupe_keep_last(filepath):
    p = Path(filepath)
    if not p.exists():
        print(f"File not found: {filepath}")
        return 1
    data = json.loads(p.read_text(encoding='utf-8'))
    songs = data.get('Songs', [])
    seen = set()
    out = []
    # iterate reversed to keep last occurrence
    for s in reversed(songs):
        key = s.get('SoundId')
        if not key:
            # fallback: use title+artist
            key = (s.get('Title','').strip().lower(), s.get('Artist','').strip().lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    out.reverse()
    data['Songs'] = out
    bak = p.with_suffix(p.suffix + '.bak')
    # create .bak if it doesn't exist
    if not bak.exists():
        bak.write_text(json.dumps(json.loads(p.read_text(encoding='utf-8')), indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"Backup created: {bak.name}")
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Deduped {len(songs)} -> {len(out)} songs. Overwrote: {p.name}")
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 dedupe_playlist.py <playlist_file.json>")
        sys.exit(1)
    sys.exit(dedupe_keep_last(sys.argv[1]))
