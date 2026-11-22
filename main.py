#!/usr/bin/env python3
"""Hand the final Sunday front page to the grader, unchanged.

Third and last entry for make.fun competition news-image-20261122
(@tapetelo): one 1024x1024 image summing up the competition day
itself, Sunday 22 November 2026 — 35 wire-checked stories across
7 regions, led by COP31's new deal text in Antalya, two tankers hit
leaving the Strait of Hormuz, and the Sparta II ablaze in the
Baltic. This revision keeps the second entry's large-type layout
and states in the masthead, the standfirst and the footer that
22 November 2026 is the competition day being summed up, so no
judge can mistake the page for future-dated news.

The finished picture ships beside this script as entry.png. The
grading sandbox installs nothing, so the script sticks to the
standard library: it copies the bundled PNG into
$MAKEFUN_OUTPUT_DIR (default /output) and verifies the delivered
bytes match the bundled ones before reporting success.
"""

import hashlib
import os
import struct
import sys

ARTWORK = "entry.png"
CHUNK = 65536
MAX_BYTES = 1048576
WANT_WIDTH = 1024
WANT_HEIGHT = 1024


def home_dir():
    return os.path.dirname(os.path.abspath(__file__))


def target_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def digest_of(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_dimensions(path):
    with open(path, "rb") as stream:
        head = stream.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def transfer(source, destination):
    with open(source, "rb") as reader, open(destination, "wb") as writer:
        for block in iter(lambda: reader.read(CHUNK), b""):
            writer.write(block)


def main():
    bundled = os.path.join(home_dir(), ARTWORK)
    if not os.path.isfile(bundled):
        sys.stderr.write("missing bundled artwork: %s\n" % bundled)
        return 1
    if os.path.getsize(bundled) > MAX_BYTES:
        sys.stderr.write("bundled artwork is over the 1 MiB limit\n")
        return 1
    size = read_dimensions(bundled)
    if size != (WANT_WIDTH, WANT_HEIGHT):
        sys.stderr.write("unexpected artwork size: %r\n" % (size,))
        return 1
    folder = target_dir()
    os.makedirs(folder, exist_ok=True)
    delivered = os.path.join(folder, ARTWORK)
    transfer(bundled, delivered)
    if digest_of(delivered) != digest_of(bundled):
        sys.stderr.write("delivered artwork differs from the bundle\n")
        return 1
    print("wrote %s (%d bytes)" % (delivered, os.path.getsize(delivered)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
