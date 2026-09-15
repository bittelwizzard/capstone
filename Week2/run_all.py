from __future__ import annotations

from pathlib import Path

from ucb_strategy import propose_query_for_function


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    for i in range(1, 9):
        _, submission = propose_query_for_function(root, i)
        print(f"Function {i}: {submission}")


if __name__ == "__main__":
    main()
