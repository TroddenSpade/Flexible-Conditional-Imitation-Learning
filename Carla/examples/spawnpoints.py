import carla

# Creating a client
client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()
for mapName in client.get_available_maps():
    print(mapName)

world = client.get_world()

#get all spawn points
spawn_points = world.get_map().get_spawn_points()
number_of_spawn_points = len(spawn_points)

print(number_of_spawn_points)

print(spawn_points)