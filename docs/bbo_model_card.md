# BBO Optimisation Model Card

## Overview

**Approach name:** Adaptive Gaussian Process Search for BBO

**Type:** Sequential black-box optimisation method

**Version:** Final project iteration, round 13

**Task:** Choose one input query for each of eight unknown functions and use the returned results to choose the next queries.

This is not a model that predicts a fixed label. It is a search method for finding high-value inputs when the function formulas are hidden and the number of evaluations is limited.

## Intended Use

The approach is suitable for:

- Black-box optimisation with unknown function formulas.
- Small data sets.
- Expensive function evaluations.
- Problems where one new query can be chosen after each result.
- Educational research into exploration and exploitation.

The approach is not suitable for:

- Safety-critical or high-stakes decisions.
- Guaranteed global optimisation.
- Problems with a large amount of training data and cheap evaluations.
- Functions with sudden changes if smooth behaviour is required.
- Situations where an evenly sampled or unbiased data set is needed.

## Details: Ten-Round Development

The project used one query per function in each round. The approach changed as the data and observed outcomes accumulated.

**Round 1:** I used Gaussian-process expected improvement, comparing several kernel choices to find possible improvements over the best known result.

**Round 2:** I moved to an exploration-weighted upper confidence bound (UCB) strategy because the early data left substantial uncertainty.

**Rounds 3–10:** I added dimension-aware candidate budgets and small adjustments to the exploration weight based on recent results. The GP used a Matern kernel with a noise term. I also ran a separate neural-network comparison, but neural networks were not used to generate submitted queries.

**Rounds 11–12:** I grouped observed inputs into clusters and gave a small preference to candidates near the group with the strongest average output, while retaining the GP uncertainty signal.

**Round 13:** With no later query round to benefit from information alone, I selected candidates by expected improvement over the best observed result. The search mixed global random candidates with local candidates near strong observations and the best cluster. It used fixed seeds, rounded candidates to the submission precision and rejected previously observed inputs.

The final query-generation code is [scripts/propose_week13_queries.py](../scripts/propose_week13_queries.py). The final proposals and diagnostics are in the [week 13 folder](../week%2013/), and their returned values are in [week 14/outputs.txt](../week%2014/outputs.txt).

## How Decisions Were Made

For each function, the approach:

1. Combined the initial observations with the previous query results.
2. Generated many possible input points between zero and one.
3. Estimated which points looked promising and which points were uncertain.
4. Balanced these two factors.
5. Selected one point as the next query.
6. Added the returned result to the data before the next round.

The main strength of this process is that it uses the limited query budget deliberately. Its main weakness is that every decision depends on the model's view of areas that have not been tested.

## Performance

The following figures compare the best initial output, best observed output after 13 rounds and the final-round output. These are optimisation outcomes, not prediction accuracy. Output scales differ by function, and a best observed value is not proof of a global optimum.

| Function | Initial best | Best observed | Final-round output |
|---|---:|---:|---:|
| 1 | ~0 | 3.76e-08 | 3.76e-08 |
| 2 | 0.611205 | 0.642454 | 0.618589 |
| 3 | -0.034835 | -0.034835 | -0.085477 |
| 4 | -4.025542 | 0.661510 | 0.576859 |
| 5 | 1088.859619 | 8662.405001 | 8662.405001 |
| 6 | -0.714265 | -0.328287 | -0.328287 |
| 7 | 1.364968 | 2.125210 | 1.880808 |
| 8 | 9.598482 | 9.969268 | 9.969268 |

The best observed output improved over the initial best for seven functions; Function 3 did not improve. Function 5 had the largest numerical gain, although its output scale cannot be compared directly with the other functions. The final result was below the best-so-far result for Functions 2, 3, 4 and 7, showing that recent performance was not uniformly improving.

The method produced valid formatted query points for all eight functions. The final generator saved its seeds and candidate settings. GP fitting emitted convergence and parameter-bound warnings for some functions; predictions and uncertainty should therefore be treated cautiously.

## Assumptions and Limitations

The approach assumes that nearby input points often have related results. This helps the model use previous observations but may fail around narrow peaks, sudden changes, thresholds or strong variable interactions. Exact repeated inputs returned different outputs in Functions 2, 3 and 6. This shows repeat variability in the records, but its source was not established.

The approach also assumes that the input range is zero to one, that results from different rounds are comparable and that the goal is to maximise the output. It treats a poor recent result as a reason to explore more, but this could overreact to one unusual result.

The main limitations are:

- The query budget is small compared with the size of the search spaces.
- Functions 6 and 8 have many variables, so their spaces are difficult to cover.
- Later queries are adaptive and are not an even sample of the search space.
- Random candidate generation can miss a narrow high-value region.
- The model may favour boundaries because several useful-looking points are near zero or one.
- Only a small number of repeated inputs are present, and the reason for output differences is unknown.
- Some GP fits reached parameter bounds or generated convergence warnings.
- Candidate scores are saved for the final round, but not consistently for every earlier round.

These limitations mean that the best observed result is not necessarily the global optimum.

## Ethical Considerations and Transparency

This project does not use personal, demographic or sensitive data. The main ethical issue is being accurate about what the results show. The main methodological risks are over-trusting sparse model predictions, adaptive sampling bias and treating an isolated high score as a reliable pattern.

The data and scripts are kept in the repository so that the query process can be reviewed and repeated. The weekly input files, output files, diagnostics and reflections show how decisions changed over time. Repeated input records with differing outputs are retained rather than silently merged.

The results should not be presented as an unbiased survey of the search space. They should also not be used to claim that the functions were fully understood. Anyone adapting the method to a real problem should record the data available at each decision, the query budget, the model settings and the uncertainty about untested regions.

## Reproducibility and Future Detail

The final proposal can be reproduced using the repository data, [scripts/propose_week13_queries.py](../scripts/propose_week13_queries.py), [requirements.txt](../requirements.txt) and the round-13 history in [week 13](../week%2013/). The final outputs are stored in [week 14](../week%2014/).

Adding more detail would improve the model card. In particular, future versions should record the date of each round, software versions, candidate-pool sizes, model settings, selected scores and the next-best candidate. This information would make it easier to explain individual decisions and compare the approach with another method.

The current structure is sufficient for a clear high-level explanation, but these extra records would improve detailed auditing and make the results more useful to someone trying to adapt the approach to another optimisation problem.
