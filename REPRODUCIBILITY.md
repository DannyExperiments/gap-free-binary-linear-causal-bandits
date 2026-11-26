# Reproducibility

From the repository root with Python 3.11 or later and Git:

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The standard-library replay uses exact fractions. It checks 1,200 rational model/action pairs, every one of the 11,368 models in the two-node, one-round grid with 34,104 action predictions, and 915 atomic-family distribution, gap and chi-square-bound cases. It independently reconstructs the illustration's three prediction pairs and its exact reward-row residual. [Expected output](verification/logs/replay.txt)

The replay checks these finite cases. The concentration and determinant arguments covering all horizons are in the proof. [Manuscript build](paper/BUILD.md) · [Figure build and explorer](visualization/README.md)
