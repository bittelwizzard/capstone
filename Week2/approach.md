# Week 2 Approach (Succinct)

## How the new query points were generated

1. Start from each function's initial data:
   - `function_n/initial_inputs.npy`
   - `function_n/initial_outputs.npy`
2. Read Week 1 portal feedback from:
   - `Week2/input.txt` (the submitted point per function)
   - `Week2/outputs.txt` (the returned score per function)
3. Append that feedback to each function's dataset, so each model uses a growing history.
4. Fit a Gaussian Process (GP) surrogate for each function.
5. Sample many candidate points in the valid domain \([0,1)\) for each dimension.
6. Score candidates with an exploration-focused UCB rule:

   \[
   \mathrm{UCB}(x) = \mu(x) + \beta\,\sigma(x)
   \]

   where:
   - \(\mu(x)\): GP predicted mean
   - \(\sigma(x)\): GP predicted uncertainty
   - \(\beta\): exploration weight (set higher for higher dimensions)
7. Select the candidate with the highest UCB value.
8. Format for portal submission as six-decimal hyphen-separated strings.

## Why this strategy

- UCB balances exploitation (high predicted score) and exploration (high uncertainty).
- With only one extra round of data, uncertainty is still high, so exploration is important.
- The method is consistent across all 8 functions while adapting to dimensionality.

## Code used

- Shared strategy: `Week2/ucb_strategy.py`
- Per-function scripts: `Week2/function_n/propose_query.py`
- Full runner: `Week2/run_all.py`

## Week 2 proposed query strings

- Function 1: 0.368897-0.715648
- Function 2: 0.999996-0.370823
- Function 3: 0.588009-0.017654-0.000677
- Function 4: 0.453082-0.441963-0.152321-0.446364
- Function 5: 0.530079-0.028606-0.984897-0.999366
- Function 6: 0.401972-0.064387-0.975333-0.999609-0.846847
- Function 7: 0.013418-0.355135-0.165985-0.075509-0.356172-0.848789
- Function 8: 0.046925-0.969544-0.021248-0.935814-0.901612-0.242645-0.043017-0.572593
