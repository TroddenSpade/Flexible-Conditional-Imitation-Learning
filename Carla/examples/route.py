import carla

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

def other_side_of_road(waypoint):
    """
    Return the waypoint on the other side of the road.
    """
    if waypoint.road_idx == 0:
        return waypoint.get_right_lane()
    else:
        return waypoint.get_left_lane()


wp = []
wp_p = []
wp_m = []

for w in w1:
    print(w)
    wp.append([w[0].transform.location.x, w[0].transform.location.y, w[0].transform.location.z])
    world.debug.draw_string(w[0].transform.location, 'O', draw_shadow=False, 
                            color=carla.Color(r=255, g=0, b=0), life_time=120.0, persistent_lines=True)

    w_p = other_side_of_road(w[0])
    wp_p.append([w_p.transform.location.x, w_p.transform.location.y, w_p.transform.location.z])
    world.debug.draw_string(w_p.transform.location, 'O', draw_shadow=False,
                            color = carla.Color(r=0, g=0, b=255), life_time=1000.0,persistent_lines=True)

    x = (w[0].transform.location.x + w_p.transform.location.x)/2
    y = (w[0].transform.location.y + w_p.transform.location.y)/2
    z = (w[0].transform.location.z + w_p.transform.location.z)/2
    l_m = carla.Location(x, y, z)
    wp_m.append([x, y, z])
    world.debug.draw_string(l_m, 'O', draw_shadow=False,
                            color = carla.Color(r=0, g=255, b=0), life_time=1000.0,persistent_lines=True)

