import carla
import numpy as np

from agents.navigation.global_route_planner import GlobalRoutePlanner

client = carla.Client("localhost", 2000)
client.set_timeout(10)
world = client.load_world('Town01')
amap = world.get_map()


sampling_resolution = 2
grp = GlobalRoutePlanner(amap, sampling_resolution)


spawn_points = world.get_map().get_spawn_points()
a = carla.Location(spawn_points[50].location)
b = carla.Location(spawn_points[100].location)

w1 = grp.trace_route(a, b)

wp = []
wp_p = []

for w in w1:
    x, y = w[0].transform.location.x, w[0].transform.location.y
    wp.append([x, y])
    world.debug.draw_string(w[0].transform.location, 'O', draw_shadow=False, 
                            color=carla.Color(r=255, g=0, b=0), life_time=120.0, persistent_lines=True)

    theta = w[0].transform.rotation.yaw * np.pi/180
    v_p, v_p = -w.lane_width * np.sin(theta), w.lane_width * np.cos(theta)
    p_p = [x + v_p, y + v_p]
    wp_p.append(p_p)
    loc = carla.Location(x=p_p[0], y=p_p[1], z=0.0)
    world.debug.draw_string(loc, 'O', draw_shadow=False,
                            color = carla.Color(r=0, g=0, b=255), life_time=1000.0,persistent_lines=True)


