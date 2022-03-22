import carla
import numpy as np

# Creating a client
client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()


world = client.load_world('Town02')

map = world.get_map()

waypoint_list = map.generate_waypoints(2.0)

coor = np.zeros((len(waypoint_list),3))

for i,w in enumerate(waypoint_list):
    coor[i,0] = w.transform.location.x
    coor[i,1] = w.transform.location.y
    coor[i,2] = w.transform.location.z

np.save('./2', coor)
