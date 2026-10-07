# Black-Box Optimisation Capstone

This repository documents a 13-round search for high-scoring inputs to eight unknown functions. It includes the data, query-generation code, final results, reflections, project documentation and a short presentation.

## Plain-Language Summary

This project used 13 rounds of experiments to find high-scoring inputs for eight functions whose formulas were hidden. Each function accepts between two and eight values and returns a score. I began with the supplied examples, then used each new result to guide the next experiment. The search moved from broad exploration to a more focused strategy that tested promising areas while retaining some uncertainty. In the final round, I selected points with a good estimated chance of improving the best result so far. The best observed score improved for seven functions; Function 5 rose from 1,088.86 to 8,662.41. These are observed results, not guaranteed global optima.

## Start Here

- [Five-page project presentation](docs/bbo_capstone_presentation.pdf)
- [Datasheet](docs/bbo_datasheet.md)
- [Model card](docs/bbo_model_card.md)
- [Repository structure guide](docs/repository_structure.md)
- [Final-round reflection](week%2013/round13_reflection.md)
- [Final submitted query points](week%2013/proposed_queries_round13.txt)
- [Final-round returned results](week%2014/outputs.txt)

## Final Results

The table compares the initial best observed output, the best observed output after 13 query rounds, and the final-round output. Output scales differ substantially between functions, so compare values within a function, not across functions.

| Function | Dimensions | Initial best | Best observed | Final-round output |
|---|---:|---:|---:|---:|
| 1 | 2 | approximately 0 | 3.76e-08 | 3.76e-08 |
| 2 | 2 | 0.611205 | 0.642454 | 0.618589 |
| 3 | 3 | -0.034835 | -0.034835 | -0.085477 |
| 4 | 4 | -4.025542 | 0.661510 | 0.576859 |
| 5 | 4 | 1088.859619 | 8662.405001 | 8662.405001 |
| 6 | 5 | -0.714265 | -0.328287 | -0.328287 |
| 7 | 6 | 1.364968 | 2.125210 | 1.880808 |
| 8 | 8 | 9.598482 | 9.969268 | 9.969268 |

These are best observed values from the available evaluations, not proof that a global optimum was found. The final query results are in the thirteenth record in `week 14/outputs.txt`.

## Method

The process used one query per function per round. I fitted a Gaussian-process surrogate to the initial observations and accumulated history, then ranked candidate points using an acquisition rule that balanced predicted value and uncertainty. The strategy evolved from expected improvement to UCB-guided search, added dimension-aware candidate budgets and trend adjustments, and later used clustering to guide local exploration. For the final round, I returned to expected improvement and mixed global candidates with candidates near strong observations and clusters.

The final generator is [scripts/propose_week13_queries.py](scripts/propose_week13_queries.py). The submission can be reproduced from the project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/propose_week13_queries.py
```

## Data and Files

The eight functions have between two and eight input dimensions. The repository contains 175 supplied initial observations and 104 query records from 13 rounds, for 279 input-output records. Initial data are in `function_1` through `function_8`; weekly inputs and outputs are kept in their original folders. The final proposal is in `week 13`, and its returned results are in `week 14`.

For example, inspect the [Function 1 initial inputs](function_1/initial_inputs.npy) and [initial outputs](function_1/initial_outputs.npy), or review the [final-round input history](week%2014/inputs.txt) and [returned values](week%2014/outputs.txt).

The initial NumPy arrays total about 10 KB, and no project dataset approaches 50 MB. The data are included directly in the repository; no external dataset link is needed. The function formulas and their real-world meanings were not provided, so this project does not assign them domain interpretations.

## Repository Layout

- `function_1` to `function_8`: supplied input/output arrays.
- `Week2`, `week3`, and `week 4` to `week 14`: query histories, outputs, proposals and reflections.
- `scripts`: query-generation and presentation code.
- `docs`: datasheet, model card, presentation and repository guide.
- `Templates`: course-provided datasheet and model-card examples.

## Environment

Dependencies are listed in [requirements.txt](requirements.txt): NumPy, SciPy, scikit-learn and PyMuPDF. Query generation uses NumPy and scikit-learn; PyMuPDF builds the presentation.

## Repository

Public project repository: [github.com/bittelwizzard/capstone](https://github.com/bittelwizzard/capstone)
