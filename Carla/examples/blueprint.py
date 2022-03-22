import carla

# Creating a client
client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()
world = client.get_world()
world = client.load_world('Town01')

blueprints = [bp for bp in world.get_blueprint_library().filter('*')]
for blueprint in blueprints:
   print(blueprint.id)
   for attr in blueprint:
       print('  - {}'.format(attr))