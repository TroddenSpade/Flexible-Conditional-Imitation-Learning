import carla
import numpy as np
import pickle
import matplotlib.pyplot as plt



# Creating a client
client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()


world = client.load_world('Town01')

map = world.get_map()

waypoint_list = map.generate_waypoints(2.0)

coor = []
roads = {}
for i,w in enumerate(waypoint_list):
    if w.road_id not in roads:
        roads[w.road_id] = []
    else:
        roads[w.road_id].append([w.transform.location.x, w.transform.location.y])

print(roads)


# with open(r'C:\Users\hp\Desktop\Autonomous-Car\Carla\waypoints\w1', 'wb') as fp:
#     pickle.dump(coor, fp)



# with open(r'C:\Users\hp\Desktop\Autonomous-Car\Carla\waypoints\pos', 'rb') as fp:
#     pos = pickle.load(fp)
# pos = np.load(r"C:\Users\hp\Desktop\Autonomous-Car\Carla\waypoints\pos.npy", allow_pickle=True)


c = 0
for k,v in roads.items():
    v = np.array(v)
    plt.scatter(v[:, 0], v[:,1], s=5)
    c+=1
    if c == 20:
        break

plt.show()