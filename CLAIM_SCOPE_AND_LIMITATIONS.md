# Scope and limitations

The algorithm assumes a known finite intervention menu, a known horizon, and full observations of the modeled binary nodes for each hard intervention. Its reward is terminal. The Markovian structural model yields fixed interventional mean recurrences with nonnegative, row-substochastic coefficients, including the intercept. Small positive coefficients are allowed.

The algorithm enumerates a finite set of acyclic coefficient models and maximizes over both models and actions. Its running time can be exponential. Polynomial-time computation using only the row-ellipsoid pair oracle, partly observed models and nonlinear mechanisms are outside the result.

The atomic-only minimax comparison applies to the null and both single-node assignments. Adding simultaneous interventions can change that minimax problem. The optimal dependence on the number of nodes for general menus remains open.

The finite replay checks exact examples of the key identities and the first-round rational grid. The manuscript proves the general regret guarantee.
