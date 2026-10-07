# Round 12 Reflection

## How My Strategy Has Evolved

In the early rounds, I used the limited data to balance promising points with less familiar areas. The process now feels more structured: I combine the previous results, use the model to compare possible queries and check that each submission is valid.

From round 11, I also grouped similar input points and gave extra attention to groups with better average results. Round 12 continued this approach using all eleven completed rounds. This helps focus the search, but a good group average can still hide poor individual points. The grouping guides the decision; it does not prove that an area is reliable.

## Patterns Behind the Largest Changes

Function 5 has shown strong results when several inputs are close to one, including the latest result of about 6672. Function 4 has shown sharp changes: two recent results were below -34, followed by a result of about -0.55 closer to the central region. Function 7 also improved to about 2.13 with several low input values.

These suggest that combinations of variables and the location of a query matter. However, I usually change several inputs together, so I cannot confidently say which individual variable caused an improvement.

This is similar to thinking about the main patterns in PCA, but I have not applied PCA to this data. I would also compare variation within each function rather than across all eight, because their output scales are very different.

## What I Would Keep or Simplify

I would keep the balance between promising areas and uncertainty, along with the grouping of similar points. I would simplify by avoiding extra settings unless they clearly improve the decisions. Group averages should remain supporting evidence rather than override individual results.

I would also avoid repeatedly testing almost identical points unless the purpose was to confirm a result. The history already includes repeated inputs, so I need to distinguish genuine repeat evaluations from duplicated records. I would not remove an input variable just because it has changed little in my queries; that may reflect my sampling choices rather than its importance.

## Planning the Final Round

The current history contains eleven completed rounds, so I still need the round-12 outputs before choosing the final queries. If the nearby tests improve Functions 2, 4, 5 or 7, I would favour another focused query in those promising areas.

For less clear functions, I would compare a local refinement with a carefully chosen alternative area. With only one round left, exploration needs a realistic chance of improving the result, not just providing information for later rounds. I would make this decision separately for each function.

## What PCA Adds to My Thinking

PCA encourages me to look for the main patterns and reduce repeated information. For BBO, this means reviewing which changes seem useful and whether similar queries are adding much evidence.

However, the largest variation is not always the most useful signal. A variable that changes little could still control a narrow peak. PCA describes variation in the inputs; it does not automatically identify what drives high outputs. I would use it as an additional way to inspect the data, not as a reason to discard variables without checking their effect on results.