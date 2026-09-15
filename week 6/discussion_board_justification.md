# Week 6 Discussion Board Response: Technical Justification for BBO Strategy

The main reason I chose my current BBO approach is that it works well when data is limited and each query is expensive. In this project, I only get one new point per function per round, so I need a method that can make careful decisions with small datasets. That is why I use a Gaussian Process surrogate with a UCB-style acquisition rule. It gives me two useful signals at once: where the model thinks value is high and where uncertainty is still high.

The biggest research influence is the Bayesian optimization line of work. The GP-UCB framework helped me justify the explore vs exploit balance in a principled way instead of doing trial-and-error search. The Gaussian Processes for Machine Learning book gave me the core intuition for posterior mean/variance behavior. I also leaned on survey-style BO material and practical BO papers focused on tuning to confirm that this family of methods is reliable under tight evaluation budgets. That matters for this capstone because it shows my strategy is grounded in established methods, not just a custom heuristic.

For tools, my core stack is NumPy plus scikit-learn. NumPy keeps data handling and candidate generation straightforward. scikit-learn gives me a stable and easy-to-audit GP implementation with Matern kernels and noise modeling. I considered PyTorch and TensorFlow for neural surrogates, but in this low-data regime they would likely add training overhead without clear upside yet. I also see BoTorch/Ax as a strong next step once I want more advanced acquisition functions, but for now scikit-learn gives me the best balance of rigor, simplicity, and speed.

In the repository, I plan to make this reasoning easy to follow for peers, facilitators, and employers. I will keep this write-up in the Week 6 folder, maintain a concise method summary in README, keep scripts reproducible with fixed seeds, and include a references block that maps each design choice to a source or package. The goal is not only to show what I submitted, but to make the technical logic behind each decision obvious and reviewable.

Looking ahead, I want to improve in three directions. For research, I want to read more on trust-region and high-dimensional BO methods like TuRBO. For benchmarking, I want tighter comparisons against random search, Sobol sampling, and CMA-ES under the same query budget. For software, I want to test BoTorch for qEI/qUCB variants and compare against practical optimizers in Optuna and Nevergrad. That combination should help me move from a solid baseline strategy to a more robust and better-validated optimization workflow.

## Sources Referenced

- GP-UCB framework from work by Srinivas, Krause, Kakade, and Seeger.
- Gaussian process foundations from the book Gaussian Processes for Machine Learning by Rasmussen and Williams.
- Bayesian optimization survey perspective from work by Shahriari, Swersky, Wang, Adams, and de Freitas.
- Practical BO tuning perspective from work by Snoek, Larochelle, and Adams.
- High-dimensional local BO direction (TuRBO) from work by Eriksson, Pearce, Gardner, Turner, and Poloczek.
