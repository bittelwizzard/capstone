import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, RBF, WhiteKernel


def expected_improvement(mu: np.ndarray, sigma: np.ndarray, best: float, xi: float = 1e-6) -> np.ndarray:
    """Compute EI for maximization."""
    improvement = mu - best - xi
    z = np.divide(improvement, sigma, out=np.zeros_like(improvement), where=sigma > 1e-12)
    return np.where(sigma > 1e-12, improvement * norm.cdf(z) + sigma * norm.pdf(z), 0.0)


def main() -> None:
    # Reproduce the exact search setup used for function_1.
    rng = np.random.default_rng(7)
    x = np.load("function_1/initial_inputs.npy")
    y = np.load("function_1/initial_outputs.npy")

    n_candidates = 150_000
    candidates = rng.uniform(0.0, 0.999999, size=(n_candidates, 2))
    best_observed = float(np.max(y))

    kernels = [
        C(1.0, (1e-4, 1e4))
        * Matern(length_scale=[0.3, 0.3], length_scale_bounds=(1e-4, 1e4), nu=1.5)
        + WhiteKernel(noise_level=1e-8, noise_level_bounds=(1e-12, 1e-2)),
        C(1.0, (1e-4, 1e4))
        * Matern(length_scale=[0.3, 0.3], length_scale_bounds=(1e-4, 1e4), nu=2.5)
        + WhiteKernel(noise_level=1e-8, noise_level_bounds=(1e-12, 1e-2)),
        C(1.0, (1e-4, 1e4))
        * RBF(length_scale=[0.3, 0.3], length_scale_bounds=(1e-4, 1e4))
        + WhiteKernel(noise_level=1e-8, noise_level_bounds=(1e-12, 1e-2)),
    ]

    best_global_ei = -np.inf
    best_point = None

    for i, kernel in enumerate(kernels, start=1):
        gp = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            n_restarts_optimizer=10,
            random_state=7 + i,
        )
        gp.fit(x, y)

        mu, sigma = gp.predict(candidates, return_std=True)
        ei = expected_improvement(mu, sigma, best_observed)
        j = int(np.argmax(ei))

        if float(ei[j]) > best_global_ei:
            best_global_ei = float(ei[j])
            best_point = candidates[j]

    if best_point is None:
        raise RuntimeError("No candidate point selected.")

    submission = f"{best_point[0]:0.6f}-{best_point[1]:0.6f}"
    print(submission)


if __name__ == "__main__":
    main()