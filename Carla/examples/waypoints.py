import carla
import numpy as np
import pickle


# Creating a client
client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()


world = client.load_world('Town01')

map = world.get_map()

waypoint_list = map.generate_waypoints(2.0)

coor = []
# roads = {}
# for i,w in enumerate(waypoint_list):

#     if w.lane_id > 0:
#         if w.road_id not in roads:
#             roads[w.road_id] = []
#         else:
#             roads[w.road_id].append([w.transform.location.x, w.transform.location.y])
# print(roads)

for i,w in enumerate(waypoint_list):
    coor.append(w.transform.location)
print(coor)


with open(r'C:\Users\hp\Desktop\Autonomous-Car\Carla\waypoints\w1', 'wb') as fp:
    pickle.dump(coor, fp)

