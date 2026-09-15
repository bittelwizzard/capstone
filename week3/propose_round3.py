from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, WhiteKernel


def parse_inputs(input_path: Path) -> tuple[list[np.ndarray], list[np.ndarray]]:
    text = input_path.read_text(encoding="utf-8")
    blocks = re.findall(r"array\(\[([^\]]+)\]\)", text, flags=re.DOTALL)

    parsed: list[np.ndarray] = []
    for block in blocks:
        nums = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", block)
        parsed.append(np.array([float(v) for v in nums], dtype=np.float64))

    if len(parsed) < 16:
        raise ValueError("Expected two rounds of 8 queries each in week3/inputs.txt")

    return parsed[:8], parsed[8:16]


def parse_outputs(output_path: Path) -> tuple[list[float], list[float]]:
    text = output_path.read_text(encoding="utf-8")
    wrapped = re.findall(r"np\.float64\(([^\)]+)\)", text)
    vals = [float(v.strip()) for v in wrapped]

    if len(vals) < 16:
        raise ValueError("Expected two rounds of 8 outputs each in week3/outputs.txt")

    return vals[:8], vals[8:16]


def candidate_budget(dim: int) -> int:
    if dim <= 2:
        return 160_000
    if dim == 3:
        return 200_000
    if dim == 4:
        return 240_000
    if dim == 5:
        return 280_000
    if dim == 6:
        return 320_000
    return 420_000


def beta_for_dim_and_trend(dim: int, y_prev: float, y_latest: float) -> float:
    # Use a modestly adaptive exploration weight:
    # increase exploration if the latest observation degraded, reduce it if improved.
    base = 2.1 + 0.28 * float(dim)
    if y_latest > y_prev:
        base -= 0.18
    else:
        base += 0.12
    return max(1.8, base)


def propose_round3_queries(root: Path) -> list[str]:
    round1_x, round2_x = parse_inputs(root / "week3" / "inputs.txt")
    round1_y, round2_y = parse_outputs(root / "week3" / "outputs.txt")

    submissions: list[str] = []
    for i in range(1, 9):
        func_dir = root / f"function_{i}"
        x_init = np.load(func_dir / "initial_inputs.npy")
        y_init = np.load(func_dir / "initial_outputs.npy")

        x_train = np.vstack((x_init, round1_x[i - 1].reshape(1, -1), round2_x[i - 1].reshape(1, -1)))
        y_train = np.append(y_init, [round1_y[i - 1], round2_y[i - 1]])

        dim = x_train.shape[1]
        rng = np.random.default_rng(42_000 + i)
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
            random_state=300 + i,
        )
        gp.fit(x_train, y_train)

        mu, sigma = gp.predict(candidates, return_std=True)
        beta = beta_for_dim_and_trend(dim, round1_y[i - 1], round2_y[i - 1])
        ucb = mu + beta * sigma
        best_idx = int(np.argmax(ucb))

        best = candidates[best_idx]
        submissions.append("-".join(f"{v:0.6f}" for v in best))

    return submissions


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    submissions = propose_round3_queries(root)
    for i, s in enumerate(submissions, start=1):
        print(f"Function {i}: {s}")


if __name__ == "__main__":
    main()
