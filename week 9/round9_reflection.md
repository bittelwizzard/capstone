# Round 9 Reflection

This round made me think more carefully about how scaling affects the search. More data and more candidate points help, but the benefit is not the same for every function.

## Scaling and Query Choices

In the two-dimensional functions, the accumulated points give me reasonably useful local coverage. In the six- and eight-dimensional functions, the same number of observations still covers only a small part of the possible search space. This means the GP becomes more informed, but it is still uncertain about many regions.

I am seeing steady improvements in the process, especially in reproducibility and in how I compare exploration with exploitation. I am also seeing diminishing returns from simply adding another observation without improving coverage. For this reason, I used larger candidate pools for higher-dimensional functions and kept the UCB acquisition rule. The UCB score gives more attention to points that might be good but are still uncertain.

The scores themselves are not improving in a perfectly steady way. Some rounds produce strong results and others expose a boundary or an unexpected drop. That unevenness is expected in a black-box problem with limited data.

## Emergent Behaviour

Emergent behaviour could appear as a threshold, an interaction between variables or a narrow high-value region. Some of the earlier outputs changed sharply after relatively small changes in the query point, so I do not want to assume that every function has a smooth global pattern.

My current preparation is to keep exploration in the acquisition rule instead of following only the highest predicted mean. I also use a Matern kernel because it is more flexible than a simple linear model, while still being manageable with the amount of data available. If a new point produces an unusually strong result, I will treat it as evidence of a possible local pattern rather than immediately assuming that I have found the global solution.

The next useful check would be to compare a promising point with nearby points and with a point from a different region. That would help distinguish a real interaction from a lucky or isolated observation.

## Cost, Robustness and Performance

Each black-box query is expensive because I only receive one new point per function in a round. A poor guess therefore costs more than local computer time spent fitting the model. I stayed with a GP because it fits the current data size quickly, gives an uncertainty estimate and is easier to inspect than a larger neural network.

The main trade-off is between searching widely and concentrating on known good areas. Pure exploitation could give a better immediate prediction, but it could also repeat a model error. Pure exploration would improve coverage but ignore useful evidence from previous rounds. The UCB rule gives me a practical balance between these two choices.

I also kept fixed random seeds, bounded all coordinates and checked the formatting before accepting the queries. These details do not directly increase the objective value, but they improve robustness and make the experiment reproducible.

## Predictable Optimisation and Uneven Emergence

I am treating the optimisation loop as the predictable part of the process: fit the surrogate, estimate uncertainty, score candidate points and validate the final output. Hidden interactions and sudden changes are the less predictable part. I want to allow for them without letting one surprising output completely change the strategy.

In practice, I use the strongest observed signals while reserving some query opportunity for uncertain regions. I would only move heavily toward exploitation after seeing repeated evidence that the same region is valuable. A sudden high output should be followed by nearby or contrastive tests before I treat it as a dependable pattern.

This approach may miss an occasional lucky opportunity, but it reduces the risk of repeatedly following an outlier. After nine iterations, my main conclusion is that scaling the amount of computation helps, but it does not replace good coverage. The next improvement should come from using local structure and confirming unexpected behaviour, rather than only increasing the model size or candidate budget.