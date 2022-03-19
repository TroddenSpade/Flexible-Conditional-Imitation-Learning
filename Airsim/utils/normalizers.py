import numpy as np

def normalize_points(set_of_points, speeds, z_rotate):
    s = set_of_points - set_of_points[0]
    diffs = s[1:] - s[:-1]
    norm_speed = (speeds[1:] + speeds[:-1])/2
    norm_diffs = diffs / np.expand_dims(norm_speed, axis=-1)
    s = np.cumsum(norm_diffs, axis=0)
    R = np.array([[np.cos(z_rotate), -np.sin(z_rotate)],
                  [np.sin(z_rotate), np.cos(z_rotate)]])
    s = s @ R    
    return s

