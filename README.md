# BBO Capstone Project

This repository records a black-box optimisation study across ten rounds. The task is to choose one query point for each of eight unknown functions, observe the returned scalar values and use those results to choose the next queries.

The project is organised around the data, query history, reproducible scripts and written analysis. It does not depend on a hosted service or a deployed application.

## Project Goal

Find high-value query points under tight evaluation budgets when function formulas are unknown.

The optimization loop is:
1. Propose one query per function.
2. Receive outputs.
3. Update surrogate beliefs.
4. Propose the next round.

## Function Dimensions

- Function 1: 2D
- Function 2: 2D
- Function 3: 3D
- Function 4: 4D
- Function 5: 4D
- Function 6: 5D
- Function 7: 6D
- Function 8: 8D

Submission format per function:
- `x1-x2-...-xn`
- Each value is six decimals and starts with `0` (for example: `0.123456-0.654321`)

## Documentation

- [BBO data sheet](docs/bbo_datasheet.md): contents, collection, uses and maintenance of the query data.
- [BBO model card](docs/bbo_model_card.md): optimisation approach, performance, assumptions and limitations.
- [Repository structure guide](docs/repository_structure.md): locations of data, scripts and round records.
- [Round 10 reflection](week%2010/round10_reflection.md): final-round reasoning and critical evaluation.

## Repository Structure

- `function_1` to `function_8`: initial input and output arrays.
- `Week2` through `week 10`: round inputs, outputs, proposal files and reflections.
- `scripts`: reproducible query-generation scripts.
- `docs`: the data sheet, model card and repository guide.
- `hyperparameters.md`: supporting experiments comparing surrogate choices.
- `*.ipynb`: separate course assignments, not part of the BBO query loop.

## Current Optimization Strategy

The current approach is Gaussian Process Regression with a UCB acquisition rule.

- Surrogate: `GaussianProcessRegressor` with Matern kernel.
- Acquisition: `UCB = mean + beta * std`.
- Adaptation: beta scales with dimension and adjusts slightly from recent performance trend.
- Candidate search: random candidate pool sampled in `[0, 1)` per dimension.

Why this is used:
- Strong uncertainty handling with very small datasets.
- Stable behaviour in early, data-sparse rounds.
- Easy to inspect and debug between submission rounds.

## Libraries and Tools

Core packages:
- `numpy`
- `scikit-learn`
- `scipy`

These are listed in `requirements.txt`.

## Reproducibility

### 1. Environment

From the project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Generate the latest query set

```powershell
.venv\Scripts\python.exe scripts/propose_week10_queries.py
```

Optional output file:

```powershell
.venv\Scripts\python.exe scripts/propose_week10_queries.py --out "week 10\proposed_queries_round10.txt"
```

## Project Records

The weekly folders preserve the original round records and reflections. The root-level lesson and assignment files are supporting course material; the active optimisation workflow is contained in the function folders, weekly BBO records, `scripts` and `docs`.
