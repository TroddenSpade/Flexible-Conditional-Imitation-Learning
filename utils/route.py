import os
import pandas as pd
import numpy as np

class Route:
    def __init__(self, file_name, N) -> None:
        path = os.path.join('.', 'routes', file_name)
        self.samples = pd.read_csv(path)
        self.N = N

    def get_speeds(self):
        return self.samples['Speed'].to_numpy()

    def get_coordinates(self):
        xs = self.samples["POS_X"].to_numpy()
        ys = self.samples["POS_Y"].to_numpy()
        xs = np.append(xs, np.repeat(xs[-1], self.N))
        ys = np.append(ys, np.repeat(ys[-1], self.N))
        return np.vstack((xs,ys)).T