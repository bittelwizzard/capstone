from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, WhiteKernel


def _parse_week2_inputs(input_path: Path) -> list[np.ndarray]:
    text = input_path.read_text(encoding="utf-8")
    blocks = re.findall(r"array\(\[([^\]]+)\]\)", text, flags=re.DOTALL)

    parsed: list[np.ndarray] = []
    for block in blocks:
        nums = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", block)
        parsed.append(np.array([float(v) for v in nums], dtype=np.float64))
    return parsed


def _parse_week2_outputs(output_path: Path) -> list[float]:
    text = output_path.read_text(encoding="utf-8")
    wrapped = re.findall(r"np\.float64\(([^\)]+)\)", text)
    if wrapped:
        return [float(v.strip()) for v in wrapped]

    vals = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)
    return [float(v) for v in vals]


def _candidate_budget(dim: int) -> int:
    if dim <= 2:
        return 140_000
    if dim == 3:
        return 170_000
    if dim == 4:
        return 210_000
    if dim == 5:
        return 250_000
    if dim == 6:
        return 290_000
    return 340_000


def _beta_for_dim(dim: int) -> float:
    # Exploration-focused UCB: higher dimensions get slightly stronger uncertainty weight.
    return 2.6 + 0.25 * float(dim)


def propose_query_for_function(root: Path, function_index: int) -> tuple[np.ndarray, str]:
    week2_dir = root / "Week2"
    inputs_hist = _parse_week2_inputs(week2_dir / "input.txt")
    outputs_hist = _parse_week2_outputs(week2_dir / "outputs.txt")

    if len(inputs_hist) < 8 or len(outputs_hist) < 8:
        raise ValueError("Week2 input/output history is incomplete; expected 8 entries.")

    func_dir = root / f"function_{function_index}"
    x_init = np.load(func_dir / "initial_inputs.npy")
    y_init = np.load(func_dir / "initial_outputs.npy")

    x_prev = inputs_hist[function_index - 1].reshape(1, -1)
    y_prev = float(outputs_hist[function_index - 1])

    if x_prev.shape[1] != x_init.shape[1]:
        raise ValueError(
            f"Dimension mismatch for function_{function_index}: "
            f"history has {x_prev.shape[1]}, expected {x_init.shape[1]}"
        )

    x_train = np.vstack((x_init, x_prev))
    y_train = np.append(y_init, y_prev)

    dim = x_train.shape[1]
    n_candidates = _candidate_budget(dim)
    rng = np.random.default_rng(10_000 + function_index)
    candidates = rng.uniform(0.0, 0.999999, size=(n_candidates, dim))

    kernel = (
        C(1.0, (1e-4, 1e4))
        * Matern(length_scale=np.full(dim, 0.3), length_scale_bounds=(1e-4, 1e4), nu=2.5)
        + WhiteKernel(noise_level=1e-8, noise_level_bounds=(1e-12, 1e-2))
    )
    gp = GaussianProcessRegressor(
        kernel=kernel,
        normalize_y=True,
        n_restarts_optimizer=12,
        random_state=200 + function_index,
    )
    gp.fit(x_train, y_train)

    mu, sigma = gp.predict(candidates, return_std=True)
    beta = _beta_for_dim(dim)
    ucb = mu + beta * sigma
    best_idx = int(np.argmax(ucb))
    best_point = candidates[best_idx]

    submission = "-".join(f"{v:0.6f}" for v in best_point)
    return best_point, submission
