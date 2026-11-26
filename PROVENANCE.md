# Provenance

Catalog item Q441 concerns the open regret-bound question posed after Theorem 9 of Shi Feng, Nuoya Xiong and Wei Chen's *Combinatorial Causal Bandits without Graph Skeleton*, ACML proceedings, PMLR 260 (2025), p. 283. Section 3 defines the fully observed main model. [Proceedings](https://proceedings.mlr.press/v260/feng25a.html) · [Pinned catalog entry](https://github.com/10m-u/open-problems-catalog/blob/ca8d4d44ba3db527f19f28928c240168f545ecfe/problems/statistics_data_science/experimental-design-causal-inference.md#q441)

The catalog handoff supplied the full proof, exact checks and an atomic-menu supplement. The repository records the proof in a finite rational implementation using an integer confidence threshold, a worked prediction fixture and a public replay. The [AI disclosure](AI_DISCLOSURE.md) records the technical roles.

Squared-loss confidence uses the framework of Russo and Van Roy. The atomic-menu section explicitly credits Lattimore, Lattimore and Reid's rare-root lower-bound construction and KL argument, and Audibert and Bubeck's MOSS upper bound. [Literature audit](audits/public_safe_reports/LITERATURE_AUDIT.md)
