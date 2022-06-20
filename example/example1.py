import time
from piosdk.piosdk import Pioneer
import threading

drones = []

drones.append(Pioneer(method=2, pioneer_ip="127.0.0.1", pioneer_mavlink_port=8000, logger=True))
drones.append(Pioneer(method=2, pioneer_ip="127.0.0.1", pioneer_mavlink_port=8001, logger=False))
drones.append(Pioneer(method=2, pioneer_ip="127.0.0.1", pioneer_mavlink_port=8002, logger=False))
drones.append(Pioneer(method=2, pioneer_ip="127.0.0.1", pioneer_mavlink_port=8003, logger=False))

position_object = {
    "home_drone":
        {
            'drone0': [1, 1.5, 1],
            'drone1': [1, 2.5, 1],
            'drone2': [1, 3.5, 1],
            'drone3': [1, 4.5, 1]
        },
    "points_interest":
        {
            "point0": [6.5, 8, 1],
            "point1": [6.5, 4, 1],
            "point2": [9, 6.5, 1],
            "point3": [9, 2, 1]
        }
}

mission_for_drone = [
    [
        position_object["points_interest"]["point0"],
        position_object["home_drone"]["drone0"]
    ],
    [
        position_object["points_interest"]["point1"],
        position_object["home_drone"]["drone1"]
    ],
    [
        position_object["points_interest"]["point2"],
        position_object["home_drone"]["drone2"]
    ],
    [
        position_object["points_interest"]["point3"],
        position_object["home_drone"]["drone3"]
    ]

]

for drone in drones:
    drone.arm()
    drone.takeoff()

new_point = [True, True, True, True]
while True:


    fin = 0
    for i in range(len(drones)):

        if new_point[i]:
            new_point[i] = False
            current_point = mission_for_drone[i].pop(0)
            drones[i].go_to_local_point(*current_point)

        if drones[i].point_reached():
            print('new_point', i)
            if len(mission_for_drone[i]) == 0:
                fin += 1
                continue

            new_point[i] = True

        if fin == 4:
            print('break')
            break
        fin = 0

