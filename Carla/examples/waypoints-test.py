import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle

# with open(r'C:\Users\hp\Desktop\Autonomous-Car\Carla\waypoints\pos', 'rb') as fp:
#     pos = pickle.load(fp)
# pos = np.load(r"C:\Users\hp\Desktop\Autonomous-Car\Carla\waypoints\pos.npy", allow_pickle=True)
w1 = np.load(r"C:\Users\hp\Desktop\Autonomous-Car\Carla\examples\waypoints.npy")

print(w1.shape)
print(w1)

plt.scatter(w1[:,0], w1[:,1], s=5)
# plt.scatter(w2[:,0], w2[:,1], s=5)

# print(pos.items())
# for k,v in pos.items():
#     v = np.array(v)
#     plt.scatter(v[:, 0], v[:,1], s=5)

plt.show()