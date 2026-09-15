# Round 10 Reflection

## Reasoning Behind the Submission

For round 10, I used the initial observations and all of the results from the previous rounds. I used the same model as in the earlier rounds to estimate which areas might produce good results. I balanced points that looked promising with points in areas where I had less information.

I used more possible points for the functions with more variables because those parts of the search space are harder to cover. I also kept the process consistent by using the same settings and keeping every value between zero and one. When the latest result improved, I focused slightly more on promising areas. When it became worse, I allowed more exploration.

Overall, I did not simply choose the point with the best predicted result. I used the patterns in the previous results, but also tested less familiar areas because the data were still limited.

## Transparency and Reproducibility

The decision process is reasonably clear and reproducible. Another researcher would need the original data, the previous round results and the query-generation script. They would also need the same Python packages and settings.

The final query points are recorded in the repo, so the submission can be checked. The process could be even clearer if I had recorded all of the possible points considered and explained why the final point was chosen over the next best options.

## Assumptions

My main assumption is that nearby input points will usually have similar results. This makes it possible for the model to learn from the points already tested. However, this assumption may be wrong if a function has a sudden change, a narrow peak or a hidden threshold.

I also assume that the results from each round can be compared, that all input values should be between zero and one and that the goal is to find the highest possible output. If one of these assumptions is wrong, the proposed points may not be useful.

Another assumption is that a poor recent result is a reason to explore more. That result may instead have been an unusual or noisy observation, so the strategy could sometimes react too strongly to one result.

## Data Gaps and Potential Biases

The queries are not spread evenly across the whole search space. Later points were chosen using earlier results, so areas that looked promising received more attention. Areas that looked poor at the beginning may not have been tested enough.

This is a bigger problem for functions 6 and 8 because they have more variables. The same number of observations gives much less coverage in those spaces, so a useful region could easily be missed. Some of the points are also close to zero or one in several variables. This may show a real pattern, but it could also be caused by the way the model selected points.

I also did not always test points close to a successful result. Because of this, I cannot always tell whether a high result shows a useful area or was just a lucky result. Repeating some queries would also help me decide whether unusual results were caused by noise.

## Significant Limitation

The biggest limitation is the small number of queries compared with the size of the search spaces. The model can help decide where to look next, but it cannot know about areas that have never been tested. It may also make a wrong prediction because it assumes that the functions behave in a fairly regular way.

For this reason, the proposed points are reasonable next experiments, but they do not prove that the best possible results have been found. A stronger approach would include more evenly spread points, repeat some promising queries and test points close to successful results.