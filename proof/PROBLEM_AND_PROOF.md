# Problem and proof

For an unknown fully observed binary linear causal DAG, choose sequential hard interventions from a fixed finite menu. The aim is expected cumulative regret with a square-root horizon exponent and polynomial node dependence while allowing arbitrarily small positive weights. [Exact source question](https://raw.githubusercontent.com/mlresearch/v260/main/assets/feng25a/feng25a.pdf#page=13)

1. Round the weights down on a rational grid. Preserve acyclicity and row sums, and propagate rounding error along a topological order to bound all action-mean errors.
2. Score models by cumulative squared error across all observed coordinates. Simultaneous confidence keeps an accurate rounded model plausible and bounds the selected model's discrepancy over past actions.
3. For each free node, subtract its two mean equations. The resulting row residual is the coordinate prediction error minus a weighted aggregate of all errors. Bound its squared sum in the row's past design.
4. Propagate the row residuals in the selected model's topological order. The determinant potential bounds the accumulated row widths and yields the stated regret rate under optimism.

With only null and signed atomic actions the paper separately adapts the causal-bandit KL lower bound and uses MOSS for a matching upper bound. [Complete proof](../paper/manuscript.pdf)
