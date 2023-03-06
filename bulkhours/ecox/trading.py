import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import statsmodels.api as sm
import matplotlib
from .brownian import Brown
import time


def get_test_data():
    from ..core import data

    return data.get_data_from_file("freefight.csv")


class Sampler:
    outsample_dt = None


Sampler.outsample_dt = time.time() - 100


def check_outsample(my_trading_algo):
    if (tdiff := time.time() - Sampler.outsample_dt) < 120:
        print(f"This test can be runned in {120-tdiff:.0f} seconds.")
        return

    Sampler.outsample_dt = time.time()
    print(f"Do the test {tdiff}")

    from ..core import data

    gdf = data.get_data_from_file("ffcontrol.csv")
    pos = my_trading_algo(gdf)

    pnls = pd.DataFrame()
    for i in range(8):
        pnls[f"pnl_{i}"] = gdf[f"ret_{i}"] * pos[f"pos_{i}"].shift(1)

    pnls["pnl_all"] = pnls.mean(axis=1)
    print(np.sqrt(252) * pnls.mean() / pnls.std())