import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import TransformedTargetRegressor
from sklearn.metrics import mean_squared_error

root = Path(r"c:/git/CAPSTONE")

def eval_cfg(x, y, cfg, seeds=(0,1,2,3,4)):
    rmses = []
    for s in seeds:
        xtr, xva, ytr, yva = train_test_split(x, y, test_size=0.3, random_state=s)
        base = Pipeline([
            ("sx", StandardScaler()),
            ("mlp", MLPRegressor(
                hidden_layer_sizes=cfg["hidden_layer_sizes"],
                learning_rate_init=cfg["learning_rate_init"],
                alpha=cfg["alpha"],
                max_iter=3000,
                random_state=s,
                early_stopping=True,
                n_iter_no_change=40,
                validation_fraction=0.2,
            ))
        ])
        model = TransformedTargetRegressor(regressor=base, transformer=StandardScaler())
        model.fit(xtr, ytr)
        pred = model.predict(xva)
        rmse = mean_squared_error(yva, pred) ** 0.5
        rmses.append(rmse)
    return float(np.mean(rmses)), float(np.std(rmses))

configs = [
    {"name":"small_lr1e-3","hidden_layer_sizes":(32,),"learning_rate_init":1e-3,"alpha":1e-4},
    {"name":"small_lr1e-2","hidden_layer_sizes":(32,),"learning_rate_init":1e-2,"alpha":1e-4},
    {"name":"wide_lr1e-3","hidden_layer_sizes":(128,64),"learning_rate_init":1e-3,"alpha":1e-4},
    {"name":"wide_reg","hidden_layer_sizes":(128,64),"learning_rate_init":1e-3,"alpha":1e-2},
]

for fn in [7,8,5]:
    x = np.load(root/f"function_{fn}"/"initial_inputs.npy")
    y = np.load(root/f"function_{fn}"/"initial_outputs.npy")
    print(f"Function {fn} n={len(y)} d={x.shape[1]}")
    for cfg in configs:
        m,s = eval_cfg(x,y,cfg)
        print(f"  {cfg['name']}: rmse_mean={m:.6f} rmse_std={s:.6f}")
    print()
