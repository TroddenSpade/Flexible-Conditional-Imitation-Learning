import airsim
import numpy as np
import os
import time
import tempfile
import keyboard


# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
print("API Control enabled: %s" % client.isApiControlEnabled())
car_controls = airsim.CarControls()

tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_car")
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

while True:
    # get state of the car
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))

    car_controls.throttle = 0.5
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Go Forward")

    if keyboard.is_pressed(" "):
        # if client.isRecording():
        client.enableApiControl(False)
        client.startRecording()
        time.sleep(5)
        client.stopRecording()
        client.enableApiControl(True)

client.reset()
client.enableApiControl(False)
