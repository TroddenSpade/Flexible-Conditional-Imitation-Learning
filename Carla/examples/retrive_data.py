#Dependencies
import glob
import os
import sys
import time
import numpy as np
import carla
import logging
import random
from datetime import datetime

TOWN_NAME = 'Town01'
DIRECTORY = 'Data'
IMAGE_WIDTH = 88
IMAGE_HEIGHT = 200
RECORD_LENGTH = 10


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


# --------------
# Spawn attached RGB camera
# --------------

data = {
    'image_name': [],
    'steering':[],
    'throttle':[],
    'brake':[],

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
    velocity = convert_vector_to_scalar(ego_vehicle.get_velocity())
    speed_limit = ego_vehicle.get_speed_limit()
    light_state = ego_vehicle.get_traffic_light_state()
    is_traffic_light = ego_vehicle.is_at_traffic_light()
    traffic_light = ego_vehicle.get_traffic_light()
    print(control, transform, velocity, speed_limit, light_state, is_traffic_light, traffic_light)




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


if ego_vehicle is not None:
    if ego_cam is not None:
        ego_cam.stop()
        ego_cam.destroy()
    ego_vehicle.destroy()


print("\nData retrieval finished")
print(rec_dir)