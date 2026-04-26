import sys
import json
from portfolio_ask.main import answer


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m portfolio_ask \"Your question here\"")
        print("\nExamples:")
        print("  python -m portfolio_ask \"What is my P&L?\"")
        print("  python -m portfolio_ask \"Show my sector allocation\"")
        print("  python -m portfolio_ask \"What is EBITDA?\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    result = answer(query)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
