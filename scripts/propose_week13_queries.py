from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.stats import norm
from sklearn.cluster import KMeans
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel

from propose_week11_queries import candidate_budget, parse_round_inputs, parse_round_outputs


def propose_queries(root: Path) -> tuple[list[str], list[str]]:
    history = root / "week 13"
    rounds_x = parse_round_inputs(history / "inputs.txt")
    rounds_y = parse_round_outputs(history / "outputs.txt")
    if len(rounds_x) != 12 or len(rounds_y) != 12:
        raise ValueError("Final proposals require twelve completed input-output rounds")
    if any(len(values) != 8 for values in rounds_x + rounds_y):
        raise ValueError("Every recorded round must contain eight functions")

    submissions: list[str] = []
    diagnostics: list[str] = []
    for function_index in range(1, 9):
        initial_x = np.load(root / f"function_{function_index}" / "initial_inputs.npy")
        initial_y = np.load(root / f"function_{function_index}" / "initial_outputs.npy")
        train_x = np.vstack([initial_x, [values[function_index - 1] for values in rounds_x]])
        train_y = np.concatenate([initial_y, [values[function_index - 1] for values in rounds_y]])
        dimension = initial_x.shape[1]
        if not np.isfinite(train_x).all() or not np.isfinite(train_y).all():
            raise ValueError("Non-finite training values")
        if np.any(train_x < 0) or np.any(train_x > 1):
            raise ValueError("Training input outside unit cube")

        kernel = (
            ConstantKernel(1.0, (1e-4, 1e4))
            * Matern(length_scale=np.full(dimension, 0.3), length_scale_bounds=(1e-4, 1e4), nu=2.5)
            + WhiteKernel(noise_level=1e-8, noise_level_bounds=(1e-12, 1e-2))
        )
        model = GaussianProcessRegressor(
            kernel=kernel, normalize_y=True, n_restarts_optimizer=12,
            random_state=1500 + function_index,
        )
        model.fit(train_x, train_y)

        grouping = KMeans(n_clusters=3, n_init=10, random_state=1600 + function_index)
        labels = grouping.fit_predict(train_x)
        cluster_means = np.array([train_y[labels == label].mean() for label in range(3)])
        cluster_index = int(np.argmax(cluster_means))
        unique_x, inverse = np.unique(train_x, axis=0, return_inverse=True)
        point_means = np.bincount(inverse, weights=train_y) / np.bincount(inverse)
        top_points = unique_x[np.argsort(point_means)[-3:]]
        centres = np.vstack([top_points, grouping.cluster_centers_[cluster_index]])

        rng = np.random.default_rng(130000 + function_index)
        budget = candidate_budget(dimension)
        global_count = int(0.6 * budget)
        global_candidates = rng.uniform(0.0, 0.999999, size=(global_count, dimension))
        local_count = budget - global_count
        local_centres = centres[rng.integers(len(centres), size=local_count)]
        radii = rng.choice([0.03, 0.10, 0.20], size=(local_count, 1))
        local_candidates = np.clip(
            local_centres + rng.normal(size=(local_count, dimension)) * radii,
            0.0, 0.999999,
        )
        candidates = np.round(np.vstack([global_candidates, local_candidates]), 6)
        candidates = np.minimum(candidates, 0.999999)
        output_scale = float(np.std(train_y)) or 1.0
        incumbent = float(np.max(train_y))
        best_score = -np.inf
        selected = None
        for start in range(0, len(candidates), 20000):
            batch = candidates[start:start + 20000]
            repeats = np.any(
                np.all(np.abs(batch[:, None, :] - train_x[None, :, :]) <= 0.5e-6, axis=2),
                axis=1,
            )
            mean, deviation = model.predict(batch, return_std=True)
            improvement = (mean - incumbent) / output_scale
            uncertainty = deviation / output_scale
            standardized = np.divide(
                improvement, uncertainty, out=np.zeros_like(improvement), where=uncertainty > 0,
            )
            scores = np.where(
                uncertainty > 0,
                improvement * norm.cdf(standardized) + uncertainty * norm.pdf(standardized),
                np.maximum(improvement, 0),
            )
            scores[repeats] = -np.inf
            best_index = int(np.argmax(scores))
            if scores[best_index] > best_score:
                best_score = float(scores[best_index])
                selected = batch[best_index].copy()
        if selected is None or not np.isfinite(best_score):
            raise ValueError("No novel candidate available")
        predicted, uncertainty = model.predict(selected.reshape(1, -1), return_std=True)
        nearest = float(np.min(np.linalg.norm(train_x - selected, axis=1)) / np.sqrt(dimension))
        submissions.append("-".join(f"{value:.6f}" for value in selected))
        diagnostics.append(
            f"Function {function_index}: records={len(train_y)}, unique_inputs={len(unique_x)}, "
            f"best_observed={incumbent:.8g}, latest={train_y[-1]:.8g}, "
            f"predicted_mean={predicted[0]:.8g}, predicted_std={uncertainty[0]:.8g}, "
            f"standardized_expected_improvement={best_score:.8g}, "
            f"nearest_distance={nearest:.6f}, seed={130000 + function_index}, "
            f"candidates={budget}, kernel={model.kernel_}"
        )
    return submissions, diagnostics


def main() -> None:
    parser = argparse.ArgumentParser(description="Propose the final BBO round using expected improvement")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    submissions, diagnostics = propose_queries(args.root)
    destination = args.root / "week 13"
    (destination / "proposed_queries_round13.txt").write_text("\n".join(submissions) + "\n", encoding="utf-8")
    (destination / "round13_diagnostics.txt").write_text("\n".join(diagnostics) + "\n", encoding="utf-8")
    print("\n".join(submissions))
    print("\n".join(diagnostics))


if __name__ == "__main__":
    main()