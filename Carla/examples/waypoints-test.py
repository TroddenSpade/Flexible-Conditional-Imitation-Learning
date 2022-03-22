import matplotlib
import matplotlib.pyplot as plt
import numpy as np

world1 = np.load('./Carla/examples/1.npy')

plt.scatter(world1[:100,0], world1[:100,1], s=5)
plt.show()