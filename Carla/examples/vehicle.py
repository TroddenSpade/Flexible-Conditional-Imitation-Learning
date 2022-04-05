import random
import carla

client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()
print(client.get_available_maps())

world = client.load_world('Town01')

ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
ego_bp.set_attribute('role_name','ego')
print('\nEgo role_name is set')
ego_color = random.choice(ego_bp.get_attribute('color').recommended_values)
ego_bp.set_attribute('color',ego_color)
print('\nEgo color is set')

spawn_points = world.get_map().get_spawn_points()
number_of_spawn_points = len(spawn_points)

if 0 < number_of_spawn_points:
    random.shuffle(spawn_points)
    ego_transform = spawn_points[0]
    ego_vehicle = world.spawn_actor(ego_bp,ego_transform)
    print('\nEgo is spawned')
else: 
    logging.warning('Could not found any spawn points')

print(ego_vehicle)
