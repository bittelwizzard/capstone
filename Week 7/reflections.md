# Week 7 Reflection: Hyperparameter Tuning With 16 Data Points

This round forced me to be more explicit about what I was tuning and why. With 16 points per function (10 initial + 6 iterative rounds), I now have enough signal to compare tuning decisions, but still not enough data to treat any result as fully stable.

## 1) Which hyperparameters I tuned, and why I prioritized them

I prioritized hyperparameters that directly change query quality under a tight budget:

- UCB beta schedule (exploration weight): This controls the explore vs exploit balance and has the most immediate effect on where the next query lands.
- Candidate pool size by dimension: More candidates improve the chance of finding better acquisition maxima, especially in 6D and 8D spaces.
- GP kernel/noise settings (Matern kernel with learnable length scales + WhiteKernel bounds): These control surrogate smoothness and uncertainty calibration.
- Number of optimizer restarts for GP fitting: More restarts improve kernel fit reliability at the cost of compute.

I did not prioritize broad neural surrogate tuning this round because the data regime is still small and GP-UCB gives better interpretability per query.

## 2) How tuning changed my query strategy vs earlier rounds

Earlier rounds were closer to a static strategy: fixed-style GP-UCB with limited adaptation. After tuning, the strategy became more conditional:

- I now adapt beta from recent trend information instead of using a fully fixed exploration weight.
- I use dimension-aware candidate budgets to avoid under-searching higher-dimensional functions.
- I treat uncertainty as a first-class objective rather than only chasing current predicted means.

Net effect: my queries are less reactive to a single strong or weak output and more robust across functions with different geometry.

## 3) Tuning methods used and trade-offs observed

Main methods used this round:

- Manual adjustment: I changed beta logic, restart counts, and noise/length-scale bounds based on round-to-round behavior.
- Random search in decision space: Candidate points are randomly sampled, then ranked by UCB.
- Bayesian optimization conceptually at the outer loop: The GP-UCB process itself is a Bayesian optimization policy over unknown functions.

Trade-offs:

- Manual adjustment gives strong control and interpretability, but risks human bias and overfitting to recent rounds.
- Random candidate search is simple and robust, but becomes inefficient in high dimensions unless candidate budgets grow.
- Increasing GP fitting robustness (more restarts, flexible kernels) improves stability, but raises per-round compute and can still hit boundary effects.

I did not run full grid search or Hyperband because the budget and sample size are too small for heavy meta-optimization without losing round cadence.

## 4) Model limitations that became clearer at 16 points

Tuning exposed several limitations more clearly:

- Surrogate sensitivity to sparse coverage: In higher dimensions, local uncertainty remains high and can dominate acquisition.
- Hyperparameter boundary behavior: Kernel/noise parameters sometimes push to bounds, signaling model mismatch or weak identifiability.
- Diminishing returns from single-point rounds: Each additional query helps, but improvements are increasingly uneven across functions.
- Weak calibration checks: I still rely mostly on acquisition outcomes rather than explicit uncertainty calibration diagnostics.

So while performance improved, confidence in model correctness is not improving as fast as confidence in short-term query utility.

## 5) How I would apply tuning to larger data or more complex models

For larger datasets or future ML/AI projects, I would formalize tuning into a two-level workflow:

- Inner level (model fit): Tune kernel families, noise models, and regularization with validation diagnostics.
- Outer level (query policy): Tune acquisition settings and search budgets against cumulative regret / best-found-value metrics.

Concrete upgrades:

- Replace ad hoc manual tuning with Optuna-style Bayesian search over policy and surrogate hyperparameters.
- Add trust-region BO variants (for example TuRBO) for higher-dimensional search.
- Add ablation tracking to isolate which hyperparameter changes actually improve performance.
- Use cross-round diagnostics (calibration error, residual structure, stability across seeds) before accepting a tuning change.

This would make my process less heuristic and more experiment-driven.

## 6) Professional ML/AI mindset gained from black-box tuning

This setup is a good simulation of real-world ML constraints: limited labels, incomplete system knowledge, non-stationary evidence quality, and tight evaluation budgets.

Tuning in this context trained me to:

- Make decisions under uncertainty instead of waiting for perfect information.
- Balance short-term performance with long-term information gain.
- Document rationale, assumptions, and trade-offs so choices are auditable.
- Treat reproducibility and diagnostics as part of model quality, not optional extras.

That is close to professional practice: strong outcomes matter, but so do robustness, traceability, and the ability to justify why a method should generalize beyond one good run.

## Final self-critique

My current GP-UCB strategy is a solid baseline, but still too dependent on manual heuristics for adaptation. The next step is to reduce hand-tuned logic and move toward systematic, benchmarked hyperparameter optimization with explicit calibration and robustness checks.
