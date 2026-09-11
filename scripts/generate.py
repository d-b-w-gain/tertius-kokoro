#!/usr/bin/env python3
"""Generate speech through Kokoro's OpenAI-compatible HTTP API."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default="http://localhost:8880")
    parser.add_argument("--text", default="Hello from Kokoro.")
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument(
        "--format",
        choices=("mp3", "wav", "opus", "flac", "pcm"),
        default="wav",
    )
    parser.add_argument("--output", type=Path, default=Path("output.wav"))
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--list-voices", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api = args.api.rstrip("/")

    if args.list_voices:
        with urlopen(f"{api}/v1/audio/voices", timeout=30) as response:
            payload = json.load(response)
        for voice in payload["voices"]:
            print(voice["id"])
        return

    body = json.dumps(
        {
            "model": "kokoro",
            "input": args.text,
            "voice": args.voice,
            "response_format": args.format,
            "speed": args.speed,
        }
    ).encode()
    request = Request(
        f"{api}/v1/audio/speech",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(request, timeout=180) as response:
        args.output.write_bytes(response.read())
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

