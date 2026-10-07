from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, WhiteKernel


def extract_top_lists(text: str) -> list[str]:
    chunks: list[str] = []
    depth = 0
    start: int | None = None
    for index, character in enumerate(text):
        if character == "[":
            if depth == 0:
                start = index
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0 and start is not None:
                chunks.append(text[start : index + 1])
                start = None
    return chunks


def parse_round_inputs(path: Path) -> list[list[np.ndarray]]:
    rounds: list[list[np.ndarray]] = []
    for chunk in extract_top_lists(path.read_text(encoding="utf-8")):
        vectors = []
        for block in re.findall(r"array\(\[([^\]]+)\]\)", chunk, flags=re.DOTALL):
            values = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", block)
            vectors.append(np.array([float(value) for value in values], dtype=np.float64))
        if vectors:
            rounds.append(vectors)
    return rounds


def parse_round_outputs(path: Path) -> list[list[float]]:
    rounds: list[list[float]] = []
    for chunk in extract_top_lists(path.read_text(encoding="utf-8")):
        wrapped = re.findall(r"np\.float64\(([^\)]+)\)", chunk)
        values = wrapped or re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", chunk)
        if values:
            rounds.append([float(value.strip()) for value in values])
    return rounds


def candidate_budget(dimension: int) -> int:
    return {2: 160000, 3: 200000, 4: 240000, 5: 280000, 6: 320000, 8: 440000}.get(
        dimension, 260000
    )


def propose_queries(root: Path) -> tuple[list[str], list[str]]:
    rounds_x = parse_round_inputs(root / "week 11" / "inputs.txt")
    rounds_y = parse_round_outputs(root / "week 11" / "outputs.txt")
    if len(rounds_x) != len(rounds_y) or len(rounds_x) < 2:
        raise ValueError("Week 11 inputs and outputs must contain matching prior rounds")

    submissions: list[str] = []
    diagnostics: list[str] = []
    for function_index in range(1, 9):
        initial_x = np.load(root / f"function_{function_index}" / "initial_inputs.npy")
        initial_y = np.load(root / f"function_{function_index}" / "initial_outputs.npy")
        history_x = [
            np.asarray(round_data[function_index - 1], dtype=np.float64).reshape(1, -1)
            for round_data in rounds_x
        ]
        history_y = [float(round_data[function_index - 1]) for round_data in rounds_y]
        train_x = np.vstack([initial_x] + history_x)
        train_y = np.concatenate([initial_y, np.array(history_y, dtype=np.float64)])
        dimension = train_x.shape[1]

        rng = np.random.default_rng(110000 + function_index)
        candidates = rng.uniform(0.0, 0.999999, size=(candidate_budget(dimension), dimension))
        kernel = (
            C(1.0, (1e-4, 1e4))
            * Matern(length_scale=np.full(dimension, 0.3), length_scale_bounds=(1e-4, 1e4), nu=2.5)
            + WhiteKernel(noise_level=1e-8, noise_level_bounds=(1e-12, 1e-2))
        )
        gp = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            n_restarts_optimizer=12,
            random_state=1300 + function_index,
        )
        gp.fit(train_x, train_y)

        mean, standard_deviation = gp.predict(candidates, return_std=True)
        y_scale = max(float(np.std(train_y)), 1e-12)
        ucb = (mean + (2.0 + 0.34 * dimension) * standard_deviation) / y_scale

        cluster_count = min(3, len(train_x))
        clustering = KMeans(n_clusters=cluster_count, n_init=10, random_state=1400 + function_index)
        labels = clustering.fit_predict(train_x)
        cluster_scores = np.array([
            np.mean(train_y[labels == label]) for label in range(cluster_count)
        ])
        target_cluster = int(np.argmax(cluster_scores))
        target_centroid = clustering.cluster_centers_[target_cluster]
        distances = np.linalg.norm(candidates - target_centroid, axis=1) / np.sqrt(dimension)
        cluster_affinity = np.exp(-((distances / 0.25) ** 2))
        acquisition = ucb + 0.25 * cluster_affinity
        best = candidates[int(np.argmax(acquisition))]

        submissions.append("-".join(f"{value:0.6f}" for value in best))
        nearest_observation = int(np.argmin(np.linalg.norm(train_x - best, axis=1)))
        diagnostics.append(
            f"Function {function_index}: cluster {target_cluster + 1}/{cluster_count}, "
            f"centroid distance {np.linalg.norm(best - target_centroid) / np.sqrt(dimension):.4f}, "
            f"nearest observed distance {np.linalg.norm(best - train_x[nearest_observation]) / np.sqrt(dimension):.4f}, "
            f"cluster mean {cluster_scores[target_cluster]:.6g}, latest output {history_y[-1]:.6g}."
        )

    return submissions, diagnostics


def main() -> None:
    parser = argparse.ArgumentParser(description="Propose BBO round-11 queries for functions 1-8.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--diagnostics", type=Path, default=None)
    args = parser.parse_args()

    submissions, diagnostics = propose_queries(args.root)
    output_text = "\n".join(submissions)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output_text + "\n", encoding="utf-8")
    if args.diagnostics is not None:
        args.diagnostics.parent.mkdir(parents=True, exist_ok=True)
        args.diagnostics.write_text("\n".join(diagnostics) + "\n", encoding="utf-8")
    print(output_text)
    print("\n".join(diagnostics))


if __name__ == "__main__":
    main()