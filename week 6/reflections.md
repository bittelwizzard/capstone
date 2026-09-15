# Week 6 Reflection

After round 6, I can see progress in both score quality and decision quality, but I also see where my strategy is still fragile.

## 1) Progressive feature extraction and BBO refinement

CNNs learn in stages: early layers detect simple structure, later layers combine that structure into richer patterns. I used a similar staged mindset in BBO:

- Early rounds: map the global shape and identify rough high-value regions.
- Middle rounds: detect local sensitivity by testing around strong candidates.
- Current round: combine global uncertainty and local evidence into targeted query moves.

The key influence was to stop treating each round as isolated. Like feature hierarchies in CNNs, each round should build on earlier information rather than replace it.

## 2) LeNet-style breakthroughs vs incremental capstone gains

LeNet and later CNNs were major breakthroughs, but they were enabled by many incremental improvements in architecture, data pipelines, and training practice. My capstone work is a smaller-scale version of that pattern:

- I did not switch to a totally new optimizer each week.
- I improved one part at a time: data accumulation, uncertainty weighting, beta adaptation, and candidate search reliability.
- Small upgrades compounded into better round-to-round decisions.

The parallel is that practical progress often looks evolutionary, then appears revolutionary only in hindsight.

## 3) Depth/cost/overfitting trade-offs vs explore/exploit trade-offs

I faced the same tension as CNN training trade-offs:

- More exploration is like deeper modeling capacity: it may discover better structure, but costs queries and can delay short-term gains.
- More exploitation is like overfitting to the current training set: strong near-term performance, but risk of missing better regions.

In this round, I balanced this with dimension-aware UCB and trend-aware beta updates. When recent outputs weakened, I increased exploration pressure; when signals improved, I exploited more. This was not perfect, but it reduced reactive overcorrection.

## 4) CNN components that changed my optimization thinking

Several CNN concepts shaped how I interpret model learning in BBO:

- Convolution: I treated local neighborhoods around good points as reusable local structure, similar to shared filters scanning for useful patterns.
- Pooling: I summarized noisy evidence by focusing on stable regional trends instead of single-point spikes.
- Activations: I interpreted nonlinear jumps in output as evidence that linear assumptions are insufficient, motivating nonlinear surrogates.
- Loss functions: I moved from "highest immediate value" to a richer objective that also values uncertainty reduction and consistency.

This helped me think of optimization as representation learning over the search space, not just point picking.

## 5) Edge AI deployment lessons and benchmarking success

Andrea Dunbar's deployment trade-off framing is useful for this project. In edge AI, success is not only accuracy; it is accuracy under constraints. In BBO, success should also be multi-criteria:

- Performance: best value found per function.
- Efficiency: improvement per query under strict budget.
- Robustness: ability to recover after weak rounds.
- Transparency: whether decisions are explainable and reproducible.

So my benchmark should be "high score with disciplined process," not "one lucky query." That perspective makes the capstone closer to real-world optimization practice, where reliability and interpretability matter as much as peak performance.

## Final self-critique

My current GP-UCB process is stronger than earlier rounds, but still has two limits:

- I can over-trust surrogate smoothness in regions with sparse coverage.
- I do not yet track uncertainty calibration quality explicitly.

Next improvement: add lightweight diagnostics (for example predicted-vs-observed error by round and uncertainty calibration checks) so query choices are guided by both expected gain and model trustworthiness.
