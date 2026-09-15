from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, WhiteKernel


def extract_top_lists(text: str) -> list[str]:
    """Extract top-level bracketed lists from a text blob."""
    chunks: list[str] = []
    depth = 0
    start: int | None = None

    for idx, ch in enumerate(text):
        if ch == "[":
            if depth == 0:
                start = idx
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0 and start is not None:
                chunks.append(text[start : idx + 1])
                start = None

    return chunks


def parse_round_inputs(path: Path) -> list[list[np.ndarray]]:
    text = path.read_text(encoding="utf-8")
    chunks = extract_top_lists(text)

    rounds: list[list[np.ndarray]] = []
    for chunk in chunks:
        blocks = re.findall(r"array\(\[([^\]]+)\]\)", chunk, flags=re.DOTALL)
        vectors: list[np.ndarray] = []
        for block in blocks:
            nums = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", block)
            vectors.append(np.array([float(v) for v in nums], dtype=np.float64))
        if vectors:
            rounds.append(vectors)

    return rounds


def parse_round_outputs(path: Path) -> list[list[float]]:
    text = path.read_text(encoding="utf-8")
    chunks = extract_top_lists(text)

    rounds: list[list[float]] = []
    for chunk in chunks:
        wrapped = re.findall(r"np\.float64\(([^\)]+)\)", chunk)
        if wrapped:
            rounds.append([float(v.strip()) for v in wrapped])
            continue

        vals = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", chunk)
        rounds.append([float(v) for v in vals])

    return rounds


def candidate_budget(dim: int) -> int:
    return {2: 160000, 3: 200000, 4: 240000, 5: 280000, 6: 320000, 8: 440000}.get(dim, 260000)


def propose_queries(root: Path) -> list[str]:
    rounds_x = parse_round_inputs(root / "week 5" / "inputs.txt")
    rounds_y = parse_round_outputs(root / "week 5" / "outputs.txt")

    if len(rounds_x) < 2 or len(rounds_y) < 2:
        raise ValueError("Need at least two prior rounds in week 5 inputs/outputs")

    submissions: list[str] = []
    for i in range(1, 9):
        x_init = np.load(root / f"function_{i}" / "initial_inputs.npy")
        y_init = np.load(root / f"function_{i}" / "initial_outputs.npy")

        x_hist = [np.asarray(r[i - 1], dtype=np.float64).reshape(1, -1) for r in rounds_x]
        y_hist = [float(r[i - 1]) for r in rounds_y]

        x_train = np.vstack([x_init] + x_hist)
        y_train = np.concatenate([y_init, np.array(y_hist, dtype=np.float64)])

        dim = x_train.shape[1]
        rng = np.random.default_rng(92000 + i)
        candidates = rng.uniform(0.0, 0.999999, size=(candidate_budget(dim), dim))

        kernel = (
            C(1.0, (1e-4, 1e4))
            * Matern(length_scale=np.full(dim, 0.3), length_scale_bounds=(1e-4, 1e4), nu=2.5)
            + WhiteKernel(noise_level=1e-8, noise_level_bounds=(1e-12, 1e-2))
        )

        gp = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            n_restarts_optimizer=10,
            random_state=900 + i,
        )
        gp.fit(x_train, y_train)

        mu, sigma = gp.predict(candidates, return_std=True)
        prev = y_hist[-2]
        latest = y_hist[-1]
        beta = 2.0 + 0.32 * dim + (-0.12 if latest > prev else 0.12)
        ucb = mu + beta * sigma

        best = candidates[int(np.argmax(ucb))]
        submissions.append("-".join(f"{v:0.6f}" for v in best))

    return submissions


def main() -> None:
    parser = argparse.ArgumentParser(description="Propose BBO Week 5 queries for functions 1-8.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root path (defaults to repository root)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Optional output file for query lines",
    )
    args = parser.parse_args()

    submissions = propose_queries(args.root)
    output_text = "\n".join(submissions)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output_text + "\n", encoding="utf-8")

    print(output_text)


if __name__ == "__main__":
    main()
