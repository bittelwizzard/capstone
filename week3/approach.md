# Week 3 Approach (Refined)

## Data used

For each of the 8 black-box functions, I trained on a growing dataset made of:
- `function_n/initial_inputs.npy` and `function_n/initial_outputs.npy`
- Round 1 query and output from `week3/inputs.txt` and `week3/outputs.txt`
- Round 2 query and output from `week3/inputs.txt` and `week3/outputs.txt`

## Modeling and acquisition strategy

I continued using a Gaussian Process surrogate with a Matern kernel and white-noise term, then selected points using an Upper Confidence Bound rule:

$$
\mathrm{UCB}(x) = \mu(x) + \beta\,\sigma(x)
$$

where:
- $\mu(x)$ is the GP mean prediction
- $\sigma(x)$ is posterior uncertainty
- $\beta$ is dimension-aware and mildly trend-adaptive

Key refinement for this round:
- If the latest observed score declined vs the prior round, I slightly increased $\beta$ to explore more.
- If the latest score improved, I slightly decreased $\beta$ to exploit more.

This keeps behavior adaptive without overfitting to one noisy observation.

## Week 3 Proposed Query Strings

- Function 1: 0.951197-0.113129
- Function 2: 0.752983-0.250898
- Function 3: 0.248115-0.000982-0.630283
- Function 4: 0.314622-0.426057-0.494836-0.459289
- Function 5: 0.172740-0.989344-0.997602-0.999452
- Function 6: 0.021986-0.014358-0.054820-0.964841-0.005594
- Function 7: 0.022456-0.078150-0.467483-0.007582-0.327113-0.683061
- Function 8: 0.172342-0.007942-0.291599-0.016481-0.914945-0.053280-0.040194-0.316002

## Reproducibility

Code used: `week3/propose_round3.py`
