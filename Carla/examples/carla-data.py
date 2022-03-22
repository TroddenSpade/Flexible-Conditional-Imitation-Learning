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
from IPython.display import display, clear_output


vehicle = None
cam = None

#enable logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# Creating a client
client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
client.reload_world()
for mapName in client.get_available_maps():
    print(mapName)
world = client.get_world()

#Create Folder to store data
today = datetime.now()
if today.hour < 10:
    h = "0"+ str(today.hour)
else:
    h = str(today.hour)
if today.minute < 10:
    m = "0"+str(today.minute)
else:
    m = str(today.minute)
directory = "./TESTDATA/" + today.strftime('%Y%m%d_')+ h + m + "_npy"

print(directory)

try:
    os.makedirs(directory)
except:
    print("Directory already exists")

try:
    inputs_file = open(directory + "/inputs.npy","ba+") 
    outputs_file = open(directory + "/outputs.npy","ba+")     
except:
    print("Files could not be opened")

#Spawn vehicle
#Get the blueprint concerning a tesla model 3 car
bp = world.get_blueprint_library().find('vehicle.tesla.model3')
#we attribute the role name brax to our blueprint
bp.set_attribute('role_name','brax')
#get a random color
color = random.choice(bp.get_attribute('color').recommended_values)
#put the selected color on our blueprint
bp.set_attribute('color',color)

#get all spawn points
spawn_points = world.get_map().get_spawn_points()
number_of_spawn_points = len(spawn_points)

#select a random spawn point
if 0 < number_of_spawn_points:
    random.shuffle(spawn_points)
    transform = spawn_points[0]
    #spawn our vehicle !
    vehicle = world.spawn_actor(bp,transform)
    print('\nVehicle spawned')
else: 
    #no spawn points 
    logging.warning('Could not found any spawn points')

#Adding a RGB camera sensor
WIDTH = 200
HEIGHT = 88
cam_bp = None
#Get blueprint of a camera
cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
#Set attributes 
cam_bp.set_attribute("image_size_x",str(WIDTH))
cam_bp.set_attribute("image_size_y",str(HEIGHT))
cam_bp.set_attribute("fov",str(105))
#Location to attach the camera on the car
cam_location = carla.Location(2,0,1)
cam_rotation = carla.Rotation(0,0,0)
cam_transform = carla.Transform(cam_location,cam_rotation)
#Spawn the camera and attach it to our vehicle 
cam = world.spawn_actor(cam_bp,cam_transform,attach_to=vehicle, attachment_type=carla.AttachmentType.Rigid)

#Function to convert image to a numpy array
def process_image(image):
    #Get raw image in 8bit format
    raw_image = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    #Reshape image to RGBA
    raw_image = np.reshape(raw_image, (image.height, image.width, 4))
    #Taking only RGB
    processed_image = raw_image[:, :, :3]/255
    return processed_image

#Save required data
def save_image(carla_image):
    image = process_image(carla_image)
    control = vehicle.get_control()
    location = vehicle.get_location()
    transform = vehicle.get_transform()
    velocity = vehicle.get_velocity()
    print(control, location, transform, velocity)
    '''
    bounding_box
    apply_control(vehicle_control)
    get_control()
    set_autopilot(enabled=True)
    get_speed_limit()
    get_traffic_light_state()
    is_at_traffic_light()
    get_traffic_light()
    '''
    data = [control.steer, control.throttle, control.brake]
    np.save(inputs_file, image)
    np.save(outputs_file, data)

#enable auto pilot
vehicle.set_autopilot(True)
#Attach event listeners
cam.listen(save_image)
world_snapshot = world.wait_for_tick()


try:
    i = 0
    while i < 3000:
        world_snapshot = world.wait_for_tick()
        clear_output(wait=True)
        display(f"{str(i)} frames saved")
        i += 1
except Exception as inst:
    print('\nSimulation error.')
    print(inst)
    print(inst.args)
   
if vehicle is not None:
    if cam is not None:
        cam.stop()
        cam.destroy()
    vehicle.destroy()
inputs_file.close()
outputs_file.close()
print("Data retrieval finished")
print(directory)