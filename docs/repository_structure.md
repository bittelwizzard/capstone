# Repository Structure Guide

This guide maps the data, scripts, round records and final portfolio materials in the BBO capstone repository.

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
  - Week 5 inputs, outputs and reflection.

- `week 6`, `Week 7`, `week 8`, `week 9`, `week 10`, `week 11`, `week 12`, `week 13`, `week 14`
  - Later-round inputs and outputs; some rounds also include proposals, diagnostics and reflections.
  - `week 13` contains the final query proposal; `week 14` contains its returned values.

- `docs`
  - `bbo_datasheet.md`: final data set documentation.
  - `bbo_model_card.md`: final optimisation approach and results.
  - `bbo_capstone_presentation.pdf`: five-page project presentation.
  - This repository structure guide.

- `scripts`
  - Proposal generators are available for Weeks 5, 7, 9, 10, 11 and 13.
  - Week 2 and Week 3 also contain earlier query-generation code.
  - Other weekly folders preserve submitted points and outcomes but do not have a matching standalone generator.
  - `build_bbo_presentation.py` regenerates the project presentation.

- `Templates`
  - Course-provided datasheet and model-card examples.

- `README.md`
  - Project overview, documentation links and run instructions.

## Reproducibility Convention

- Keep raw weekly artifacts in their original week folders.
- Put reusable tooling in `scripts`.
- Prefer deterministic random seeds in query generation scripts.
- Document strategy updates in markdown each week.

## Active Project Path

For the project summary, start with `README.md`. The presentation gives a concise overview, and the datasheet and model card document the data and method. Weekly folders preserve original observations; proposal scripts exist only for the rounds listed above. For rounds without a generator, the recorded files preserve the submitted queries and returned values, but may not reproduce the original selection process.
