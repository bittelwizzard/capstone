import numpy as np
from pathlib import Path
root = Path(r"c:/git/CAPSTONE")
for i in range(1,9):
    x = np.load(root/f"function_{i}"/"initial_inputs.npy")
    y = np.load(root/f"function_{i}"/"initial_outputs.npy")
    print(i, x.shape, y.shape, float(y.min()), float(y.max()))
