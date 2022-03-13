import sys
import numpy as np
import glob
import os
import cv2
import airsim
import matplotlib.pyplot as plt
import tensorflow as tf

from utils.functions import quaternion_to_euler, convergent_points, find_route_index
from utils.normalizers import normalize_points
from utils.route import Route

MODEL_PATH = 'saved_models/model-499'
ROUTE_PATH = 'r1.csv'
N = 10
RANGE = 50
INDX = 0

###### Load Route ######
route = Route(ROUTE_PATH, N)
route_speeds = route.get_speeds()
route_coordinates = route.get_coordinates()
print("Route loaded")


##### Load Model ######
print('Using model {0} for testing.'.format(MODEL_PATH))
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded")

model.save('my_model.h5')


print("press key")
cv2.waitKey()

client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()
print('Connection established!')
##### initialize controls #####
car_controls.steering = 0
car_controls.throttle = 0
car_controls.brake = 0

print("press key")
cv2.waitKey()


image_buf = np.zeros((1, 70, 254, 3))
control_buf = np.zeros((1, 4))
points_buf = np.zeros((1, 20))


def get_image():
    image_response = client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Scene, False, False)])[0]
    image1d = np.fromstring(image_response.image_data_uint8, dtype=np.uint8)
    image_rgba = image1d.reshape(image_response.height, image_response.width, 3)
    return image_rgba[60:130, 1:255, :3].astype(float) / 255.0


while (True):
    car_state = client.getCarState()

    ##### Control values #####
    control_buf[0] = np.array([car_state.speed, car_controls.throttle, car_controls.steering, car_controls.brake])

    qw = car_state.kinematics_estimated.orientation.w_val
    qx = car_state.kinematics_estimated.orientation.x_val
    qy = car_state.kinematics_estimated.orientation.y_val
    qz = car_state.kinematics_estimated.orientation.z_val

    x = car_state.kinematics_estimated.position.x_val
    y = car_state.kinematics_estimated.position.y_val

    pt = np.array([car_state.kinematics_estimated.position.x_val, car_state.kinematics_estimated.position.y_val])
    idx_route = find_route_index(pt, route_coordinates, INDX)
    INDX = idx_route
    selected_route = route_coordinates[idx_route:idx_route+N+1]
    conv_pts = convergent_points(pt, selected_route)
    _, _, yaw = quaternion_to_euler(qx, qy, qz, qw)
    points = normalize_points(conv_pts, route_speeds[idx_route:idx_route+N+1], yaw)
    
    ##### Points values #####
    points_buf[0] = points.ravel()

    ##### Image values #####
    image_buf[0] = get_image()


    model_output = model.predict([image_buf, control_buf, points_buf])
    car_controls.throttle = float(model_output[0,0])
    car_controls.steering = float((model_output[0,1] - 0.5) * 2.5)
    car_controls.brake = float(0)

    print('Throttle = {0},  Steering = {1},   Brake = {2}'.format(car_controls.throttle, car_controls.steering, car_controls.brake))
    
    client.setCarControls(car_controls)