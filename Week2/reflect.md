# Week 2 Reflection

The main strategy change this week was moving from an EI-led selection to a more exploration-weighted UCB policy. The reason was simple: after week 1, I had only one additional point per function, so posterior uncertainty was still high. In that setting, UCB gave a more explicit and controllable way to trade off predicted mean and uncertainty (through \(\beta\)), especially as dimensionality increased.

I focused more on exploration than exploitation this week. I still used the surrogate mean, but I intentionally gave more weight to uncertain regions. The trade-off was accepting some lower immediate predicted values in exchange for information gain that should improve later rounds. This was most important for higher-dimensional functions (6D and 8D), where over-exploitation can trap queries in narrow local regions too early.

I was influenced less by specific participant tactics and more by the shared class principle that early rounds should reduce uncertainty before aggressively hill-climbing. Recent outputs reinforced this: some functions improved strongly while others remained volatile, which suggested that model confidence was uneven and exploration remained valuable.

If I fit a simple linear or logistic model to one function (e.g., Function 5), the most likely violated assumptions would be linearity of the response surface, homoscedastic noise, and low interaction complexity. The observed behavior suggests nonlinearity and feature interactions that a plain linear/logistic form would miss, especially near sharp output changes.

There may be small local regions that look roughly linear, but globally the mapping appears curved and multimodal. A logistic classifier could work only for thresholded tasks (for example, output above vs below a chosen cutoff), and performance would depend heavily on where that threshold sits. It would likely underperform in complex boundary regions without nonlinear features.

Interpretability was still useful: inspecting individual feature ranges and whether outputs tended to rise near boundaries helped avoid naive random sampling. But I treated single-feature effects as weak guidance only; query selection was driven mainly by multivariate surrogate predictions plus uncertainty.
