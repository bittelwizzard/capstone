# Repository Structure Guide

This document explains where to find the data, scripts, round records and reports in the BBO capstone repository.

## Top-Level Layout

- `function_1` to `function_8`
  - Initial datasets for each hidden function.
  - Files: `initial_inputs.npy`, `initial_outputs.npy`.

- `Week2`
  - Week 2 submission artifacts and strategy notes.
  - Includes `input.txt`, `outputs.txt`, approach and reflection docs.

- `week3`
  - Week 3 submission artifacts, approach documents, and helper scripts.

- `week 4`
  - Week 4 inputs, outputs, and reflective analysis.

- `week 5`
  - Week 5 inputs/outputs plus current reflection.

- `week 6`, `Week 7`, `week 8`, `week 9`, `week 10`
  - Later-round inputs, outputs, proposal files and reflections.

- `docs`
  - `bbo_datasheet.md`: data set documentation.
  - `bbo_model_card.md`: optimisation approach documentation.
  - This repository structure guide.

- `scripts`
  - Reproducible query proposal scripts.
  - Includes the round-5, round-7, round-9 and round-10 generators.

- `README.md`
  - Project overview, documentation links and run instructions.

- `hyperparameters.md`
  - Hyperparameter study notes and implications for surrogate model design.

## Reproducibility Convention

- Keep raw weekly artifacts in their original week folders.
- Put reusable tooling in `scripts`.
- Prefer deterministic random seeds in query generation scripts.
- Document strategy updates in markdown each week.

## Active Project Path

For the current workflow, start with `README.md`, then read the data sheet and model card. Use the weekly folders for raw observations and the scripts for reproducible query generation. Root-level course assignments and lesson references are retained as supporting material and are separate from the BBO workflow.
