#!/usr/bin/env python3
"""Count tokens per context source and compare the total with a token budget.

Usage:
  count_tokens.py [--budget N] [--encoding NAME] SOURCE=PATH [SOURCE=PATH ...]

SOURCE is a label such as instructions, tools, knowledge, or memory. PATH is a
file or a directory (all files inside it, recursively). The same SOURCE may
appear several times. Prints a JSON object to stdout and exits 0, or exits 2
on bad arguments.

Tokens are counted with tiktoken when it is installed. Otherwise the script
estimates one token per four characters, rounded up per file, and says so in
the "method" field.
"""

import argparse
import json
import math
import sys
from pathlib import Path


def make_counter(encoding_name):
    try:
        import tiktoken
    except ImportError:
        return "estimate:chars/4", lambda text: math.ceil(len(text) / 4)
    encoding = tiktoken.get_encoding(encoding_name)
    return f"tiktoken:{encoding_name}", lambda text: len(encoding.encode(text, disallowed_special=()))


def parse_source(value):
    label, sep, path = value.partition("=")
    if not sep or not label.strip() or not path.strip():
        raise argparse.ArgumentTypeError(f"expected SOURCE=PATH, got {value!r}")
    return label.strip(), Path(path.strip())


def files_of(path):
    if path.is_dir():
        return sorted(p for p in path.rglob("*") if p.is_file())
    return [path]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count tokens per context source.")
    parser.add_argument("--budget", type=int, default=None, help="token budget for one model call")
    parser.add_argument("--encoding", default="o200k_base", help="tiktoken encoding name")
    parser.add_argument("sources", nargs="+", type=parse_source, metavar="SOURCE=PATH")
    args = parser.parse_args(argv)

    for _, path in args.sources:
        if not path.exists():
            parser.error(f"path not found: {path}")

    method, count = make_counter(args.encoding)
    totals = {}
    for label, path in args.sources:
        entry = totals.setdefault(label, {"source": label, "files": 0, "tokens": 0})
        for file in files_of(path):
            text = file.read_text(encoding="utf-8", errors="replace")
            entry["files"] += 1
            entry["tokens"] += count(text)

    total = sum(entry["tokens"] for entry in totals.values())
    result = {
        "method": method,
        "budget": args.budget,
        "sources": list(totals.values()),
        "total": total,
        "over_budget": None if args.budget is None else total > args.budget,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
