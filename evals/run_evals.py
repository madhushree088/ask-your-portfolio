"""
Run eval cases from cases.yaml. Prints PASS / FAIL per case.

Usage:
    python evals/run_evals.py
"""
import sys
import yaml
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from portfolio_ask.main import answer


def check(result: dict, checks: list[dict]) -> tuple[bool, str]:
    for c in checks:
        key = c["key"]
        val = result.get(key)

        if c.get("type") == "exists":
            if val is None:
                return False, f"Key '{key}' missing in response"

        if c.get("type") == "list_nonempty":
            if not isinstance(val, list) or len(val) == 0:
                return False, f"Key '{key}' is not a non-empty list"

        if "contains" in c:
            if not isinstance(val, list) or c["contains"] not in val:
                return False, f"Key '{key}' does not contain '{c['contains']}'"

    return True, "OK"


def main():
    cases_path = Path(__file__).parent / "cases.yaml"
    cases = yaml.safe_load(cases_path.read_text())["cases"]

    passed = 0
    print(f"\nRunning {len(cases)} eval cases...\n")

    for case in cases:
        cid = case["id"]
        query = case["query"]
        try:
            result = answer(query)
            ok, reason = check(result, case["checks"])
        except Exception as e:
            ok, reason = False, str(e)

        status = "PASS [OK]" if ok else f"FAIL [X] ({reason})"
        print(f"[{cid}] {query!r:50s} -> {status}")
        if ok:
            passed += 1

    print(f"\n{'='*60}")
    print(f"Result: {passed}/{len(cases)} passed")
    print('='*60)

    sys.exit(0 if passed == len(cases) else 1)


if __name__ == "__main__":
    main()
