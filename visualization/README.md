# Interventional means

The coordinates of the cube are the exact means of X, Z and Y. The green circle is the reference model and the violet diamond is a candidate model. Each state compares the same intervention in both models. The candidate places Z before X and the reference places X before Z.

When X is set to one, the reference means are (1.00, 0.60, 0.60) and the candidate means are (1.00, 0.20, 0.74). The models agree on the clamped coordinate. The candidate's reward error is 0.14 = 0.22 + 0.20 × (−0.40), where 0.22 is its reward-row residual. The true means are shown for teaching. The actual learner records sampled node outcomes.

Extract the ZIP and open index.html in a browser. The three controls switch between interventions. Drag horizontally or use the range control to rotate the cube.

From the repository root run `python3 visualization/render.py` with Python, Pillow and Arial fonts. If the fonts are elsewhere, set `Q441_FONT_DIR` to the directory containing Arial.ttf and Arial Bold.ttf. The renderer writes the GIF and offline ZIP. The exact numeric fixture is independently reconstructed by the standard-library replay.
