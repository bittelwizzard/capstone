from __future__ import annotations
from pathlib import Path
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, Matern, WhiteKernel

root = Path(r'c:/git/CAPSTONE')

round_x = [
[
np.array([0.70131 , 0.438738]),
np.array([0.70486 , 0.104388]),
np.array([0.998217, 0.374265, 0.809976]),
np.array([0.424664, 0.426776, 0.345475, 0.430605]),
np.array([0.214361, 0.8921  , 0.998237, 0.997109]),
np.array([0.460661, 0.30521 , 0.441997, 0.977143, 0.136686]),
np.array([0.014872, 0.408192, 0.059443, 0.418603, 0.39046 , 0.748147]),
np.array([0.051141, 0.149683, 0.041048, 0.095333, 0.947592, 0.500783, 0.065321, 0.819802]),
],
[
np.array([0.368897, 0.715648]),
np.array([0.999996, 0.370823]),
np.array([0.588009, 0.017654, 0.000677]),
np.array([0.453082, 0.441963, 0.152321, 0.446364]),
np.array([0.530079, 0.028606, 0.984897, 0.999366]),
np.array([0.401972, 0.064387, 0.975333, 0.999609, 0.846847]),
np.array([0.013418, 0.355135, 0.165985, 0.075509, 0.356172, 0.848789]),
np.array([0.046925, 0.969544, 0.021248, 0.935814, 0.901612, 0.242645, 0.043017, 0.572593]),
],
[
np.array([0.951197, 0.113129]),
np.array([0.752983, 0.250898]),
np.array([0.248115, 0.000982, 0.630283]),
np.array([0.314622, 0.426057, 0.494836, 0.459289]),
np.array([0.17274 , 0.989344, 0.997602, 0.999452]),
np.array([0.021986, 0.014358, 0.05482 , 0.964841, 0.005594]),
np.array([0.022456, 0.07815 , 0.467483, 0.007582, 0.327113, 0.683061]),
np.array([0.172342, 0.007942, 0.291599, 0.016481, 0.914945, 0.05328 , 0.040194, 0.316002]),
],
]

round_y = [
[-9.77908017021486e-30,0.632667844934265,-0.05545458584545323,0.4670208664924904,3210.47190539512,-0.46909382810049094,1.244040621504906,9.9164991696246],
[8.243071796589139e-53,0.0734122563883319,-0.17948510645376126,-4.4107996815570445,1665.1668034426016,-1.6624062075736084,0.9938297898610444,8.5489725514661],
[-4.28930702960394e-258,0.36947714413917654,-0.15793507621564823,-2.0048363631499018,4260.429667711712,-1.5675076166432111,1.6002618737260588,9.6078764243591],
]


def budget(d:int)->int:
    return {2:140000,3:180000,4:220000,5:260000,6:300000,8:380000}.get(d,220000)

subs=[]
for i in range(1,9):
    x_init=np.load(root/f'function_{i}'/'initial_inputs.npy')
    y_init=np.load(root/f'function_{i}'/'initial_outputs.npy')

    X=np.vstack([x_init, round_x[0][i-1].reshape(1,-1), round_x[1][i-1].reshape(1,-1), round_x[2][i-1].reshape(1,-1)])
    y=np.concatenate([y_init, np.array([round_y[0][i-1], round_y[1][i-1], round_y[2][i-1]], dtype=np.float64)])
    d=X.shape[1]

    rng=np.random.default_rng(62000+i)
    cand=rng.uniform(0.0,0.999999,size=(budget(d),d))

    kernel=(C(1.0,(1e-4,1e4))*Matern(length_scale=np.full(d,0.3),length_scale_bounds=(1e-4,1e4),nu=2.5)+WhiteKernel(noise_level=1e-8,noise_level_bounds=(1e-12,1e-2)))
    gp=GaussianProcessRegressor(kernel=kernel,normalize_y=True,n_restarts_optimizer=8,random_state=500+i)
    gp.fit(X,y)

    mu,s=gp.predict(cand,return_std=True)
    prev=round_y[1][i-1]
    latest=round_y[2][i-1]
    beta=2.0+0.30*d
    beta += -0.15 if latest>prev else 0.15

    ucb=mu+beta*s
    best=cand[int(np.argmax(ucb))]
    subs.append('-'.join(f'{v:0.6f}' for v in best))

for idx,s in enumerate(subs,1):
    print(f'Function {idx}: {s}')
