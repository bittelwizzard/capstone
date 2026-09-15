# BBO Optimisation Model Card

## Overview

**Approach name:** Adaptive Gaussian Process Search for BBO

**Type:** Sequential black-box optimisation method

**Version:** 1.0, used for the tenth query round

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

The project used one query per function in each round. The method developed as more results became available.

**Early rounds:** I used the initial observations to learn the general scale and behaviour of each function. The first queries were more exploratory because there was very little information about the search space.

**Middle rounds:** I began using the previous query results more directly. I compared promising results with less familiar areas and adjusted the search instead of selecting points at random. The main goal was to balance trying likely good areas with improving coverage.

**Later rounds:** I used a Gaussian process to estimate which candidate points looked promising and which areas were still uncertain. I used an upper confidence bound to combine these two ideas. This meant that the approach did not always choose the point with the highest predicted result.

**Rounds 8 to 9:** The candidate pools were increased for functions with more input variables. This was intended to reduce the chance of missing useful areas in the larger search spaces. I also paid more attention to boundary behaviour and possible interactions between variables.

**Round 10:** I used all available initial and previous-round observations. I used fixed random seeds, kept every input between zero and one and made a small adjustment based on whether the latest result improved or worsened. A worsening result led to more exploration; an improving result led to slightly more focus on promising areas.

The round-10 process is recorded in [scripts/propose_week10_queries.py](../scripts/propose_week10_queries.py). The reflections in [week 10/round10_reflection.md](../week%2010/round10_reflection.md) explain the decisions and concerns in more detail.

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

The following figures use the initial outputs and the nine recorded round-10 history evaluations. The main metrics were the best observed output and the output from the latest recorded round. These are search metrics, not prediction accuracy or proof of finding a global optimum.

| Function | Best observed output | Latest recorded output | Initial best output |
|---|---:|---:|---:|
| 1 | 0.000000 | 0.000000 | 0.000000 |
| 2 | 0.632668 | -0.133267 | 0.611205 |
| 3 | -0.034835 | -0.063980 | -0.034835 |
| 4 | 0.661510 | -34.856150 | -4.025542 |
| 5 | 4718.699964 | 3951.071060 | 1088.859618 |
| 6 | -0.469094 | -2.403142 | -0.714265 |
| 7 | 1.970877 | 1.970877 | 1.364968 |
| 8 | 9.916499 | 9.853338 | 9.598482 |

The strongest results were recorded for Functions 5, 7 and 8. Function 2 also produced a positive result. Functions 1, 3 and 6 remained weak in the recorded data. Function 4 showed unstable behaviour: it reached a positive value earlier but had a much lower latest result.

The method also produced valid formatted query points for all eight functions. It kept the inputs in the required range and used fixed settings so the round-10 queries could be reproduced.

## Assumptions and Limitations

The approach assumes that nearby input points often have related results. This allows the model to learn from previous queries. The assumption may fail when a function has a narrow peak, a sudden change, a threshold or strong variable interactions.

The approach also assumes that the input range is zero to one, that results from different rounds are comparable and that the goal is to maximise the output. It treats a poor recent result as a reason to explore more, but this could overreact to one unusual result.

The main limitations are:

- The query budget is small compared with the size of the search spaces.
- Functions 6 and 8 have many variables, so their spaces are difficult to cover.
- Later queries are adaptive and are not an even sample of the search space.
- Random candidate generation can miss a narrow high-value region.
- The model may favour boundaries because several useful-looking points are near zero or one.
- There were no repeated measurements to check unusual results.
- The method did not save every candidate score or runner-up choice.

These limitations mean that the best observed result is not necessarily the global optimum.

## Ethical Considerations and Transparency

This project does not use personal, demographic or sensitive data. The main ethical issue is being accurate about what the results show.

The data and scripts are kept in the repository so that the query process can be reviewed and repeated. The weekly input files, output files and reflections show how decisions changed over time. This supports transparency because another researcher can see both the successful results and the failed or weak queries.

The results should not be presented as an unbiased survey of the search space. They should also not be used to claim that the functions were fully understood. Anyone adapting the method to a real problem should record the data available at each decision, the query budget, the model settings and the uncertainty about untested regions.

## Reproducibility and Future Detail

The approach can be reproduced using the repository data, [scripts/propose_week10_queries.py](../scripts/propose_week10_queries.py), [requirements.txt](../requirements.txt) and the recorded query files.

Adding more detail would improve the model card. In particular, future versions should record the date of each round, software versions, candidate-pool sizes, model settings, selected scores and the next-best candidate. This information would make it easier to explain individual decisions and compare the approach with another method.

The current structure is sufficient for a clear high-level explanation, but these extra records would improve detailed auditing and make the results more useful to someone trying to adapt the approach to another optimisation problem.
