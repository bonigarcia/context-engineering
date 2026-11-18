"""Promptfoo Python assertions for the skills evaluation harness.

Every skill ends its report with a fenced json block. These functions parse
the last such block and compare it with the expectations in the test vars.
"""

import json
import re

SEVERITIES = {"high", "medium", "low"}
JSON_BLOCK = re.compile(r"```json\s*\n(.*?)\n\s*```", re.DOTALL)


def extract_json_block(output):
    blocks = JSON_BLOCK.findall(output or "")
    if not blocks:
        raise ValueError("no JSON block")
    return json.loads(blocks[-1])


def _result(passed, score, reason):
    return {"pass": passed, "score": score, "reason": reason}


def _matches(item, finding):
    location = str(finding.get("location", "")).lower()
    wanted_location = str(item.get("location", "")).lower()
    if wanted_location and wanted_location not in location:
        return False
    text = " ".join(str(finding.get(k, "")) for k in ("location", "problem", "fix")).lower()
    for keyword in item.get("keywords", []):
        options = [option.strip().lower() for option in str(keyword).split("|")]
        if not any(option in text for option in options):
            return False
    return True


def _describe(item):
    where = f" at {item['location']}" if item.get("location") else ""
    return "/".join(str(k) for k in item.get("keywords", [])) + where


def _load(output):
    try:
        data = extract_json_block(output)
    except ValueError as error:
        return None, _result(False, 0.0, str(error))
    if not isinstance(data, dict):
        return None, _result(False, 0.0, "JSON block is not an object")
    return data, None


def check_report(output, context):
    data, failure = _load(output)
    if failure:
        return failure
    findings = data.get("findings")
    if not isinstance(findings, list):
        return _result(False, 0.0, "JSON block has no findings list")

    problems = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            return _result(False, 0.0, f"finding {index} is not an object")
        if str(finding.get("severity", "")).lower() not in SEVERITIES:
            problems.append(f"finding {index} has invalid severity {finding.get('severity')!r}")

    variables = context.get("vars", {})
    required = variables.get("required") or []
    matched = 0
    for item in required:
        if any(_matches(item, finding) for finding in findings):
            matched += 1
        else:
            problems.append(f"missing required finding: {_describe(item)}")
    for item in variables.get("forbidden") or []:
        if any(_matches(item, finding) for finding in findings):
            problems.append(f"forbidden finding present: {_describe(item)}")
    for key, expected in (variables.get("extra") or {}).items():
        allowed = expected if isinstance(expected, list) else [expected]
        if data.get(key) not in allowed:
            problems.append(f"{key} is {data.get(key)!r}, expected {' or '.join(repr(a) for a in allowed)}")

    score = matched / len(required) if required else 1.0
    if problems:
        return _result(False, score, "; ".join(problems))
    return _result(True, score, f"{matched}/{len(required)} required findings present")


def check_cases(output, context):
    data, failure = _load(output)
    if failure:
        return failure
    cases = data.get("cases")
    if not isinstance(cases, list):
        return _result(False, 0.0, "JSON block has no cases list")
    variables = context.get("vars", {})
    minimum = int(variables.get("min_cases", 0))
    problems = []
    if len(cases) < minimum:
        problems.append(f"{len(cases)} cases, expected at least {minimum}")
    present = {str(case.get("category", "")).lower() for case in cases}
    categories = variables.get("categories") or []
    if isinstance(categories, str):
        categories = [item.strip() for item in categories.split(",") if item.strip()]
    for category in categories:
        if category.lower() not in present:
            problems.append(f"no case in category {category}")
    if problems:
        return _result(False, 0.0, "; ".join(problems))
    return _result(True, 1.0, f"{len(cases)} cases covering {sorted(present)}")


def _flatten(items):
    return " ".join(json.dumps(item) if not isinstance(item, str) else item for item in items or []).lower()


def check_design(output, context):
    """memory-designer: preferences go to long-term memory, booking progress to state."""
    data, failure = _load(output)
    if failure:
        return failure
    design = data.get("design")
    if not isinstance(design, dict):
        return _result(False, 0.0, "JSON block has no design object")
    long_term = _flatten(design.get("long_term_memory"))
    state = _flatten((design.get("workflow_state") or []) + (design.get("session_state") or []))
    problems = []
    if "seat" not in long_term and "preference" not in long_term:
        problems.append("long_term_memory does not hold the user preferences")
    if "booking" not in state and "step" not in state:
        problems.append("workflow_state and session_state do not hold the booking progress")
    if problems:
        return _result(False, 0.0, "; ".join(problems))
    return _result(True, 1.0, "preferences in long-term memory, booking progress in state")


def check_activation(output, context):
    answer = (output or "").strip().strip("`").strip().rstrip(".").strip().strip("`").lower()
    expected = str(context.get("vars", {}).get("expected", "")).lower()
    return _result(answer == expected, 1.0 if answer == expected else 0.0, f"answered {answer!r}, expected {expected!r}")
