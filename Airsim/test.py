from tensorflow.keras.models import load_model
import sys
import numpy as np
import glob
import os
import cv2
import airsim
import matplotlib.pyplot as plt

if ('../../PythonClient/' not in sys.path):
    sys.path.insert(0, '../../PythonClient/')
# from AirSimClient import *
cv2.waitKey()
# << Set this to the path of the model >>
# If None, then the model with the lowest validation loss from training will be used
MODEL_PATH = None

if (MODEL_PATH == None):
    models = glob.glob('./model/models/*.h5') 
    best_model = max(models, key=os.path.getctime)
    MODEL_PATH = r'D:\Users\Parsa Sam\Documents\GitHub\Autonomous-Car\Airsim\model\models\model_model.52-0.0002465.h5'
    
print('Using model {0} for testing.'.format(MODEL_PATH))
print("press key")
cv2.waitKey()



model = load_model(MODEL_PATH)

print("Model loaded")
print("press key")
cv2.waitKey()


client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()
print('Connection established!')

print("press key")
cv2.waitKey()


car_controls.steering = 0
car_controls.throttle = 0
car_controls.brake = 0

image_buf = np.zeros((1, 59, 255, 3))
state_buf = np.zeros((1,4))

print("press key")
cv2.waitKey()



def get_image():
    image_response = client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Scene, False, False)])[0]
    image1d = np.fromstring(image_response.image_data_uint8, dtype=np.uint8)
    image_rgba = image1d.reshape(image_response.height, image_response.width, 3)
    return image_rgba[76:135,0:255,0:3].astype(float) / 255.0

print("We got here")

while (True):
    car_state = client.getCarState()
    
    if (car_state.speed < 5):
        car_controls.throttle = 0.5
    else:
        car_controls.throttle = 0.0
    
    image_buf[0] = get_image()
    state_buf[0] = np.array([car_controls.steering, car_controls.throttle, car_controls.brake, car_state.speed])
    model_output = model.predict([image_buf, state_buf])
    print(model_output)
    car_controls.steering = round(0.5 * float(model_output[0][0]), 2)
    
    print('Sending steering = {0}, throttle = {1}'.format(car_controls.steering, car_controls.throttle))
    
    client.setCarControls(car_controls)