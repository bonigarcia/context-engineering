from __future__ import annotations

import argparse


def build_output(auto_approve: bool) -> str:
    lines = [
        "# Human approval",
        "",
        "Awaiting approval before publishing the synthesized brief.",
    ]
    if auto_approve:
        lines.extend([
            "",
            "Approved.",
        ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-approve", action="store_true")
    args = parser.parse_args()
    print(build_output(args.auto_approve))


if __name__ == "__main__":
    main()
