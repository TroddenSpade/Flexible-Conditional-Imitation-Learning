import numpy as np

def quaternion_to_euler(q_x, q_y, q_z, q_w):
    # t0 = +2.0 * (q_w * q_x + q_y * q_z)
    # t1 = +1.0 - 2.0 * (q_x * q_x + q_y * q_y)
    # roll_x = np.arctan2(t0, t1)
    
    # t2 = +2.0 * (q_w * q_y - q_z * q_x)
    # np.clip(t2, -1.0, +1.0)
    # pitch_y = np.arcsin(t2)
    
    t3 = +2.0 * (q_w * q_z + q_x * q_y)
    t4 = +1.0 - 2.0 * (q_y * q_y + q_z * q_z)
    yaw_z = np.arctan2(t3, t4)
    
    return None, None, yaw_z


def nearest(point, set_of_points):
    diff = np.square(set_of_points - point)
    diff = diff.sum(axis=1)
    return np.argmin(diff)


def find_route_index(pt, route, idx, range=50):
    idx_ = nearest(pt, route[idx:idx+range])
    idx = idx_ + idx
    return idx


def convergent_points(pt, selcted_route):
    l = len(selcted_route)
    v = pt - selcted_route[0]
    r = np.linspace((1,1), (0,0), l)
    v = r * v
    s = selcted_route + v
    return s