#Dependencies
from email import header
import glob
import os
import sys
import time
import numpy as np
import carla
import logging
import random
import pandas as pd
from datetime import datetime

from agents.navigation.global_route_planner import GlobalRoutePlanner

from generate_traffic import generate_traffic


TOWN_NAME = 'Town01'
DIRECTORY = 'Data'
IMAGE_WIDTH = 88
IMAGE_HEIGHT = 200
RECORD_LENGTH = 2000


def get_actor_blueprints(world, filter, generation):
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2]:
            bps = [x for x in bps if int(x.get_attribute('generation')) == int_generation]
            return bps
        else:
            print("   Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []



# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
print('\nStarted at =', dt_string)

rec_dir = os.path.join(DIRECTORY, dt_string)
image_dir = os.path.join(rec_dir, 'images')
try:
    os.makedirs(image_dir)
    print("\n"+ rec_dir + ' created')
except Exception as inst:
    print("\nError: ")
    print(inst)


client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()

world = client.load_world(TOWN_NAME)
print('\n'+ TOWN_NAME + ' Loaded.')


ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
ego_bp.set_attribute('role_name','ego')
ego_color = random.choice(ego_bp.get_attribute('color').recommended_values)
ego_bp.set_attribute('color',ego_color)

spawn_points = world.get_map().get_spawn_points()
number_of_spawn_points = len(spawn_points)

if 0 < number_of_spawn_points:
    random.shuffle(spawn_points)
    ego_transform = spawn_points[0]
    ego_vehicle = world.spawn_actor(ego_bp,ego_transform)
    print('\nVehicle is spawned')
else: 
    print('\nCould not found any spawn points!')





logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

vehicles_list = []
walkers_list = []
all_id = []

synchronous_master = False
random.seed(int(time.time()))

traffic_manager = client.get_trafficmanager(8000)
traffic_manager.set_global_distance_to_leading_vehicle(2.5)
traffic_manager.set_hybrid_physics_mode(True)
traffic_manager.set_hybrid_physics_radius(70.0)

# settings = world.get_settings()
# world.apply_settings(settings)

print("You are currently in asynchronous mode. If this is a traffic simulation, \
you could experience some issues. If it's not working correctly, switch to synchronous \
mode by using traffic_manager.set_synchronous_mode(True)")


blueprintsWalkers = get_actor_blueprints(world, 'walker.pedestrian.*', '2')

blueprints = get_actor_blueprints(world, 'vehicle.*', 'All')
blueprints = [x for x in blueprints if int(x.get_attribute('number_of_wheels')) == 4]
blueprints = [x for x in blueprints if not x.id.endswith('microlino')]
blueprints = [x for x in blueprints if not x.id.endswith('carlacola')]
blueprints = [x for x in blueprints if not x.id.endswith('cybertruck')]
blueprints = [x for x in blueprints if not x.id.endswith('t2')]
blueprints = [x for x in blueprints if not x.id.endswith('sprinter')]
blueprints = [x for x in blueprints if not x.id.endswith('firetruck')]
blueprints = [x for x in blueprints if not x.id.endswith('ambulance')]

blueprints = sorted(blueprints, key=lambda bp: bp.id)

spawn_points = world.get_map().get_spawn_points()
number_of_spawn_points = len(spawn_points)
number_of_vehicles = 100

if number_of_vehicles < number_of_spawn_points:
    random.shuffle(spawn_points)
elif number_of_vehicles > number_of_spawn_points:
    msg = 'requested %d vehicles, but could only find %d spawn points'
    logging.warning(msg, number_of_vehicles, number_of_spawn_points)
    number_of_vehicles = number_of_spawn_points

# @todo cannot import these directly.
SpawnActor = carla.command.SpawnActor
SetAutopilot = carla.command.SetAutopilot
FutureActor = carla.command.FutureActor

# --------------
# Spawn vehicles
# --------------
batch = []
for n, transform in enumerate(spawn_points):
    if n >= number_of_vehicles:
        break
    blueprint = random.choice(blueprints)
    if blueprint.has_attribute('color'):
        color = random.choice(blueprint.get_attribute('color').recommended_values)
        blueprint.set_attribute('color', color)
    if blueprint.has_attribute('driver_id'):
        driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
        blueprint.set_attribute('driver_id', driver_id)
    blueprint.set_attribute('role_name', 'autopilot')

    # spawn the cars and set their autopilot and light state all together
    batch.append(SpawnActor(blueprint, transform)
        .then(SetAutopilot(FutureActor, True, traffic_manager.get_port())))

for response in client.apply_batch_sync(batch, synchronous_master):
    if response.error:
        logging.error(response.error)
    else:
        vehicles_list.append(response.actor_id)

# -------------
# Spawn Walkers
# -------------
# some settings
percentagePedestriansRunning = 0.0      # how many pedestrians will run
percentagePedestriansCrossing = 0.5     # how many pedestrians will walk through the road
world.set_pedestrians_seed(0)
random.seed(0)
# 1. take all the random locations to spawn
number_of_walkers = 10
spawn_points = []
for i in range(number_of_walkers):
    spawn_point = carla.Transform()
    loc = world.get_random_location_from_navigation()
    if (loc != None):
        spawn_point.location = loc
        spawn_points.append(spawn_point)
# 2. we spawn the walker object
batch = []
walker_speed = []
for spawn_point in spawn_points:
    walker_bp = random.choice(blueprintsWalkers)
    # set as not invincible
    if walker_bp.has_attribute('is_invincible'):
        walker_bp.set_attribute('is_invincible', 'false')
    # set the max speed
    if walker_bp.has_attribute('speed'):
        if (random.random() > percentagePedestriansRunning):
            # walking
            walker_speed.append(walker_bp.get_attribute('speed').recommended_values[1])
        else:
            # running
            walker_speed.append(walker_bp.get_attribute('speed').recommended_values[2])
    else:
        print("Walker has no speed")
        walker_speed.append(0.0)
    batch.append(SpawnActor(walker_bp, spawn_point))
results = client.apply_batch_sync(batch, True)
walker_speed2 = []
for i in range(len(results)):
    if results[i].error:
        logging.error(results[i].error)
    else:
        walkers_list.append({"id": results[i].actor_id})
        walker_speed2.append(walker_speed[i])
walker_speed = walker_speed2
# 3. we spawn the walker controller
batch = []
walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
for i in range(len(walkers_list)):
    batch.append(SpawnActor(walker_controller_bp, carla.Transform(), walkers_list[i]["id"]))
results = client.apply_batch_sync(batch, True)
for i in range(len(results)):
    if results[i].error:
        logging.error(results[i].error)
    else:
        walkers_list[i]["con"] = results[i].actor_id
# 4. we put together the walkers and controllers id to get the objects from their id
for i in range(len(walkers_list)):
    all_id.append(walkers_list[i]["con"])
    all_id.append(walkers_list[i]["id"])
all_actors = world.get_actors(all_id)

# wait for a tick to ensure client receives the last transform of the walkers we have just created
world.wait_for_tick()


# 5. initialize each controller and set target to walk to (list is [controler, actor, controller, actor ...])
# set how many pedestrians can cross the road
world.set_pedestrians_cross_factor(percentagePedestriansCrossing)
for i in range(0, len(all_id), 2):
    # start walker
    all_actors[i].start()
    # set walk to random point
    all_actors[i].go_to_location(world.get_random_location_from_navigation())
    # max speed
    all_actors[i].set_max_speed(float(walker_speed[int(i/2)]))

print('spawned %d vehicles and %d walkers, press Ctrl+C to exit.' % (len(vehicles_list), len(walkers_list)))

# Example of how to use Traffic Manager parameters
traffic_manager.global_percentage_speed_difference(30.0)


# --------------
# Spawn attached RGB camera
# --------------

car_locations = []

data = {
    'image_name': [],
    'steer':[],
    'throttle':[],
    'brake':[],
    'speed':[],
    'x':[],
    'y':[],
    'z':[],
    'yaw':[],
    'speed_limit':[],
    'is_traffic_light':[],
    'traffic_light_state':[],
    'GPS_index':[],
}


def convert_vector_to_scalar(carlavect):
    # print(carlavect.length(), np.sqrt(carlavect.dot(carlavect)))
    # assert carlavect.length() == np.sqrt(carlavect.dot(carlavect))
    return carlavect.length()


def data_handler(image):
    img_name = dt_string + '_' + str(image.frame) + '.jpg'
    image.save_to_disk(os.path.join(image_dir, img_name))

    control = ego_vehicle.get_control()
    transform = ego_vehicle.get_transform()
    velocity = ego_vehicle.get_velocity().length()
    speed_limit = ego_vehicle.get_speed_limit()
    light_state = ego_vehicle.get_traffic_light_state()
    is_traffic_light = ego_vehicle.is_at_traffic_light()
    traffic_light = ego_vehicle.get_traffic_light()
    data['image_name'].append(img_name)
    data['steer'].append(control.steer)
    data['throttle'].append(control.throttle)
    data['brake'].append(control.brake)
    data['speed'].append(velocity)
    data['x'].append(transform.location.x)
    data['y'].append(transform.location.y)
    data['z'].append(transform.location.z)
    data['yaw'].append(transform.rotation.yaw)
    data['speed_limit'].append(speed_limit)
    data['is_traffic_light'].append(is_traffic_light)
    data['traffic_light_state'].append(light_state)

    car_locations.append(ego_vehicle.get_location())




cam_bp = None
cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
cam_bp.set_attribute("image_size_x",str(IMAGE_HEIGHT))
cam_bp.set_attribute("image_size_y",str(IMAGE_WIDTH))
cam_bp.set_attribute("fov",str(105))
cam_location = carla.Location(2,0,1)
cam_rotation = carla.Rotation(0,0,0)
cam_transform = carla.Transform(cam_location,cam_rotation)
ego_cam = world.spawn_actor(cam_bp,cam_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)


ego_vehicle.set_autopilot(True)
print('\nEgo autopilot enabled')

ego_cam.listen(data_handler)
world_snapshot = world.wait_for_tick()

try:
    i = 1
    while i <= RECORD_LENGTH:
        world_snapshot = world.wait_for_tick()
        print(f"Frame {str(i)} saved")
        i += 1

except Exception as inst:
    print('\nSimulation error:')
    print(inst)


df = pd.DataFrame(data=data)
df.to_csv(os.path.join(rec_dir, 'data.csv'), index=False)


if ego_vehicle is not None:
    if ego_cam is not None:
        ego_cam.stop()
        ego_cam.destroy()
    ego_vehicle.destroy()

time.sleep(0.5)
    
print('\ndestroying %d vehicles' % len(vehicles_list))
client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])

# stop walker controllers (list is [controller, actor, controller, actor ...])
for i in range(0, len(all_id), 2):
    all_actors[i].stop()

print('\ndestroying %d walkers' % len(walkers_list))
client.apply_batch([carla.command.DestroyActor(x) for x in all_id])

time.sleep(0.5)

print("\nSimulation finished")

print("\nSetting Waypoints' Coordinates")
map = world.get_map()
sampling_resolution = 2
grp = GlobalRoutePlanner(map, sampling_resolution)

def other_side_of_road(waypoint):
    """
    Return the waypoint on the other side of the road.
    """
    if waypoint.road_idx == 0:
        return waypoint.get_right_lane()
    else:
        return waypoint.get_left_lane()

waypoints = []
waypoints_p = []
waypoints_m = []

for idx, loc in enumerate(car_locations):

    i = idx + 1
    if i >= len(car_locations):
        break
    while car_locations[i].distance(car_locations[idx]) < 100:
        i += 1

    w1 = grp.trace_route(car_locations[idx], car_locations[i])

    wp = []
    wp_p = []
    wp_m = []

    for w in w1:
        print(w)
        wp.append([w[0].transform.location.x, w[0].transform.location.y, w[0].transform.location.z])

        w_p = other_side_of_road(w[0])
        wp_p.append([w_p.transform.location.x, w_p.transform.location.y, w_p.transform.location.z])

        x = (w[0].transform.location.x + w_p.transform.location.x)/2
        y = (w[0].transform.location.y + w_p.transform.location.y)/2
        z = (w[0].transform.location.z + w_p.transform.location.z)/2
        l_m = carla.Location(x, y, z)
        wp_m.append([x, y, z])
    
    waypoints.append(wp)
    waypoints_p.append(wp_p)
    waypoints_m.append(wp_m)


print("\nData retrieval finished")
print(rec_dir)

np.save(os.path.join(rec_dir, 'waypoints'), waypoints)
np.save(os.path.join(rec_dir, 'waypoints_p'), waypoints_p)
np.save(os.path.join(rec_dir, 'waypoints_m'), waypoints_m)
 