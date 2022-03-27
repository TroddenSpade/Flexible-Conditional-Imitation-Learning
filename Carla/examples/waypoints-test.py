import matplotlib
import matplotlib.pyplot as plt
import numpy as np

world1 = np.load(r"C:\Users\hp\Desktop\Autonomous-Car\Carla\waypoints\1.npy")

plt.scatter(world1[:,0], world1[:,1], s=5)
plt.show()