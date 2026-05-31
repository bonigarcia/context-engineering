from __future__ import annotations

import argparse


def draft_response() -> str:
    return "Draft response: keep the answer short and context-aware."


def get_approver(auto_approve: bool) -> str:
    if auto_approve:
        return "auto reviewer"
    answer = input("Press Enter to approve and continue: ").strip()
    return answer or "human reviewer"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-approve", action="store_true")
    args = parser.parse_args()

    draft = draft_response()
    print("# Human approval")
    print(draft)
    print("Awaiting approval...")
    approver = get_approver(args.auto_approve)
    print(f"Approved by {approver}.")


if __name__ == "__main__":
    main()
