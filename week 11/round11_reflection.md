# Round 11 Reflection

## Strategy

For round 11, I combined the initial observations with all ten previous rounds. I fit the same Matern Gaussian process used in the later rounds, but added an explicit clustering check. For each function, I grouped the observed input points into three coordinate-space clusters (or fewer when necessary), selected the cluster with the highest mean output, and measured each candidate's normalized distance to that cluster centroid. The final acquisition score was standardized GP-UCB plus a small centroid-affinity term. This keeps the output scale of Function 5 from overpowering the other functions while still rewarding local movement toward a promising region.

## Submitted Queries and Local Justification

| Function | Query | Local cluster and distance cue | How it sharpens the search |
|---|---|---|---|
| 1 | `0.156970-0.266877` | Targets cluster 1. The centroid distance is 0.0708 and the nearest observed distance is 0.0528, so this is a tight local probe. | Function 1 has outputs effectively at zero; after ten rounds, local confirmation is more useful than a large unexplained jump. |
| 2 | `0.796406-0.220305` | Targets cluster 2, whose mean output is 0.400557. The centroid distance is 0.0390, indicating strong boundary tightening around the best local group. | This follows the positive region seen in earlier rounds while retaining the GP-UCB uncertainty term instead of simply repeating the best point. |
| 3 | `0.412415-0.747623-0.353865` | Targets cluster 2. The centroid distance is 0.0400, while the nearest observed point is 0.0915 away; this is a local interpolation with some novelty. | Function 3 remains mostly negative, so the query tests whether the cluster trend improves away from the exact prior points. |
| 4 | `0.303580-0.429015-0.359319-0.410273` | Targets cluster 1. The centroid distance is 0.0723 and the nearest observed distance is 0.0554. | The function has been unstable, including an earlier positive result and much lower later values. This is a controlled return to a promising local group rather than trusting the latest outlier. |
| 5 | `0.999233-0.938183-0.999967-0.943157` | Targets cluster 3, the strongest-output cluster, but the centroid distance is 0.3008. The larger separation is intentional because GP uncertainty still rewards a nearby unexplored edge of this high-value region. | Function 5 produced the largest gains in the first ten rounds; this concentrates on its high-output boundary while checking whether the apparent peak has room to expand. |
| 6 | `0.596642-0.056498-0.081495-0.998030-0.020696` | Targets cluster 3. Its centroid distance is 0.1802 and nearest observed distance is 0.2103, making this the most exploratory local-cluster probe. | Function 6 has weak and variable results in five dimensions. The query uses the cluster signal but preserves more distance and uncertainty exploration where coverage is sparse. |
| 7 | `0.066879-0.102225-0.152865-0.222453-0.333978-0.530992` | Targets cluster 2, with centroid distance 0.1359 and nearest observed distance 0.0713. | Function 7 has shown strong isolated results, so this tests a nearby basin rather than assuming one high point defines the optimum. |
| 8 | `0.227077-0.360274-0.118079-0.417725-0.967220-0.459114-0.058283-0.789675` | Targets cluster 1. The centroid distance is 0.1124 and nearest observed distance is 0.1534, combining cluster proximity with a new location in the sparse eight-dimensional space. | Function 8 already has consistently strong outputs, so the main improvement is boundary and neighborhood coverage rather than aggressive exploitation of one observed point. |

## Relation to the First Ten Rounds

The first ten rounds progressively moved from broad random coverage to GP-UCB-guided exploration and exploitation. Round 11 keeps that model and candidate-budget scaling, but makes the local geometry explicit. Small centroid distances create boundary-tightening probes around strong groups; larger distances are reserved for higher-dimensional or poorly covered functions. The approach still assumes that nearby points tend to have related outputs, so sudden thresholds, narrow peaks and strong interactions remain important limitations.

The proposal is reproducible with `scripts/propose_week11_queries.py`. The generated diagnostics are stored in `round11_cluster_diagnostics.txt` beside this reflection.
