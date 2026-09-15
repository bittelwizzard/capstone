from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
WEEK2 = Path(__file__).resolve().parents[1]
if str(WEEK2) not in sys.path:
    sys.path.insert(0, str(WEEK2))

from ucb_strategy import propose_query_for_function


def main() -> None:
    _, submission = propose_query_for_function(ROOT, 3)
    print(submission)


if __name__ == "__main__":
    main()
