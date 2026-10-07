# Final Round Reflection

## Final Submission Strategy

I used the initial observations and all twelve completed rounds to prepare one new point for each function. The final query points are saved in [proposed_queries_round13.txt](proposed_queries_round13.txt). They are ready for submission; their outputs are not yet available.

For this round, I kept the Gaussian process model but changed how I ranked the possible points. Instead of giving extra weight to uncertainty mainly for future learning, I focused on the expected chance and size of an improvement over the best result already observed. This still allows a riskier point when it has useful potential, but there is no later round to benefit from information alone.

I searched both across the full input range and near strong observations and promising groups. The clustering helped decide where to generate local points; it no longer added a separate bonus to their final scores. I kept the random seeds fixed, checked the points after rounding and excluded previously tested inputs.

| Function | Reason for the final choice |
|---|---|
| 1 | The recent outputs are extremely small. The point tests a different nearby location, but the model's predicted uncertainty is not proof of a useful region. |
| 2 | Round 12 produced a new best result. The query keeps the first input near that successful point while changing the second. |
| 3 | The query tests an upper-bound region for the second input while changing the third, where the model sees potential to improve on the negative best value. |
| 4 | The query returns close to earlier successful central points rather than the boundary regions that produced large negative results. |
| 5 | Two recent high results supported another boundary-focused query, this time with all four inputs just below one. |
| 6 | The latest result approached the earlier best. The query tests a new combination that the model predicts could improve on both. |
| 7 | The latest query weakened, so the final point is closer to the earlier high-output observation rather than simply following the latest point. |
| 8 | The query uses a new combination informed by strong earlier observations rather than staying near the weaker round-12 result. |

## Exploration and Exploitation

Early on, exploration was useful because each new result could improve several later decisions. With more data, I became more selective about taking risks. I learned that a large uncertain area was not automatically worth a query, and that a promising group did not guarantee a successful individual point.

For the final round, I leaned towards improvement rather than information gathering. However, I did not just repeat the best points. I compared nearby changes with alternatives across the full space, using the same improvement rule for all eight functions. This balance remains dependent on the model and may still miss a narrow peak.

## Feedback and Reward Expectations

More data gave me better comparisons, but the feedback was uneven. Function 5 improved to about 6814 in round 12, while Function 7 dropped from about 2.13 to 1.20. These results encouraged me to continue refining Function 5's strong area while reconsidering where to search for Function 7.

This is similar to an RL agent updating its reward expectations after trying an action. In my case, each output updated the model's view of likely performance. I did not calculate Q-values or learn a policy for a sequence of actions. The analogy is about learning from feedback, not a claim that I used reinforcement learning.

## AlphaGo Zero and Autonomous Learning

The repeated cycle of choosing a point, receiving feedback and updating the model resembles autonomous learning. However, it was not self-play like AlphaGo Zero: there was no opponent, game tree or generated game experience. I also made manual choices about the method and its settings.

My process was closer to model-based planning than model-free trial and error. I used a model to anticipate the value of untested points before choosing them. Those predictions can be wrong, especially in poorly covered regions, so actual function evaluations remained the deciding evidence.

## How RL Could Help Real-World Optimisation

For repeated real-world tasks, such as adjusting shipping operations, an RL policy could learn when to try a new setting and when to reuse a reliable one. It could account for delayed rewards, costs and consequences across several decisions, rather than treating each query as an isolated experiment.

Simulation, uncertainty-guided exploration and safety limits could reduce the cost of risky trials. However, training an RL system would need much more interaction data than this project provides. For a fixed function and a small budget, a simpler bandit or Bayesian optimisation approach may be more efficient. RL is most useful when decisions change future conditions, not just the immediate output.

## Remaining Limitations

The model fitting produced convergence warnings, and some fitted settings reached their allowed bounds. Its uncertainty estimates have not been independently calibrated. The repeated inputs in the history were retained, with their provenance still unresolved; averaging their outputs was used only to select local search centres, not to replace the raw training records.

A high observed value could also be unusually favourable, which would make it a difficult target for the improvement rule. The final points are therefore reasoned experiments, not guaranteed improvements. Their success can only be assessed after the final outputs are returned.