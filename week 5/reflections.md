# Week 5 Reflection

This week I tried to be more intentional about both optimization and communication.

## Strategy Summary

I continued with a Gaussian Process + UCB workflow and kept the process adaptive:
- Use uncertainty-aware search instead of pure exploitation.
- Increase exploration when recent performance drops.
- Keep stronger exploration pressure in higher dimensions.

## Critical Reflection

- I treated the search in layers: first find broad promising regions, then refine locally.
- Small improvements from each round are compounding into a clearer model of each function.
- I still face a constant trade-off between searching widely and doubling down on known good areas.

The strongest conceptual bridge from neural network training was thinking in terms of feedback and updates:
- New outputs act like loss feedback.
- Local sensitivity behaves like directional gradient hints.
- The surrogate updates are analogous to parameter updates after each batch.

## Framework Mindset

My current process is closer to rapid prototyping than production engineering.

That is good for learning fast, but not enough for deployment-level rigor. To improve this, I need:
1. Better experiment tracking.
2. Cleaner script organization.
3. Standardized run commands and documented dependencies.

## Success Criteria Going Forward

I am benchmarking success as more than one lucky high score.

A good strategy should be:
- Consistent across rounds.
- Robust after weak rounds.
- Transparent enough that another person can reproduce my submissions.
