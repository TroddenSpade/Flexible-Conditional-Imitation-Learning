import numpy as np
import carla

client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()
print(client.get_available_maps())

world = client.load_world('Town01')