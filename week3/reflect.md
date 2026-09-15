# Week 3 Reflection (Neural Network Hyperparameters)

## Hyperparameter effects

Some key neural-network hyperparameters I used or tested are:
- `hidden_layer_sizes` (network width/depth)
- `learning_rate_init`
- `alpha` (L2 regularization)
- `max_iter`, `early_stopping`, and `n_iter_no_change`

I ran small MLP tests on existing capstone data (Functions 5, 7, and 8) with repeated train/validation splits.

Observed examples:
- Function 8 (40 points, 8D): increasing learning rate from $10^{-3}$ to $10^{-2}$ improved average RMSE from about 0.710 to 0.512 and reduced variance across splits.
- Function 7 (30 points, 6D): a small model (`(32,)`) was slightly better than a wider model (`(128, 64)`), which suggests larger capacity can overfit at this data size.
- Function 5 (20 points, 4D): errors were very large and unstable across all settings, showing that output scale and limited data can dominate behavior more than architecture tweaks.

These tests showed me that hyperparameters strongly affect convergence and stability, but their impact depends on dataset size, output scale, and dimension.

## Discrete vs continuous

Hyperparameters I used can be grouped as:

Continuous:
- `learning_rate_init`
- `alpha`
- `validation_fraction`

Discrete:
- `hidden_layer_sizes` (choice of layer counts and units)
- `max_iter` (integer)
- `n_iter_no_change` (integer)
- `early_stopping` (boolean)

Why this matters for tuning:
- Continuous hyperparameters are often tuned with Bayesian optimization, random search on log scales, or gradient-free methods over ranges.
- Discrete hyperparameters are usually tuned with grid/random search over candidate sets.
- Mixed spaces (continuous + discrete) are common in neural nets, so practical tuning often uses hybrid methods (for example, random search with Bayesian refinement).

## Application to the capstone

If I use a neural network surrogate in the capstone, these results change my next decisions:
- I will start with smaller networks in low-data settings to reduce overfitting risk.
- I will tune learning rate early, because it had clear effects on both error and stability.
- I will normalize inputs and scale targets by default, especially for functions with large output ranges (like Function 5).
- I will rely on early stopping and repeated validation splits instead of a single split.

I can also apply the BBO approach directly to neural-network tuning:
- Treat each hyperparameter set as a black-box query.
- Use validation metric (for example, RMSE) as the objective.
- Use an acquisition rule to pick the next hyperparameters, balancing exploration (untested settings) and exploitation (best known settings).

So the same BBO logic used for function optimization can directly improve neural-network performance, especially when evaluations are expensive and noisy.
