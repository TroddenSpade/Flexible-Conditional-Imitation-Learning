import os
from datetime import datetime

def create_dir(path):
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    print('\nStarted at =', dt_string)

    rec_dir = os.path.join(path, dt_string)
    image_dir = os.path.join(rec_dir, 'images')
    try:
        os.makedirs(image_dir)
        print("\n"+ rec_dir + ' created')
    except Exception as inst:
        print("\nError: ")
        print(inst)