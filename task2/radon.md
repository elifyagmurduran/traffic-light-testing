
PS C:\Users\hiromi\Documents\GitHub\traffic-light-testing\task2> python -m radon cc src/traffic_light.py -s -a
src/traffic_light.py                            
    M 11:4 TrafficLight.execute_cycle - B (7)
    M 90:4 TrafficLight.apply_manual_override - B (6)
    M 76:4 TrafficLight.is_safe_state - A (5)
    M 41:4 TrafficLight.check_synchronization - A (4)
    M 54:4 TrafficLight.manual_override - A (4)
    M 66:4 TrafficLight.apply_time_based_schedule - A (4)
    C 3:0 TrafficLight - A (3)
    M 36:4 TrafficLight.red_clearance_phase - A (3)
    M 47:4 TrafficLight.emergency_preemption - A (3)
    M 29:4 TrafficLight.yellow_transition - A (2)
    M 61:4 TrafficLight.power_failure_recovery - A (2)
    M 83:4 TrafficLight.set_all_red - A (2)
    M 4:4 TrafficLight.__init__ - A (1)
    M 73:4 TrafficLight.get_opposite_direction - A (1)
    M 87:4 TrafficLight.is_manual_mode - A (1)
    M 105:4 TrafficLight.set_green - A (1)
    M 108:4 TrafficLight.set_red - A (1)
    M 111:4 TrafficLight.set_yellow - A (1)

18 blocks (classes, functions, methods) analyzed.
Average complexity: A (2.8333333333333335)
PS C:\Users\hiromi\Documents\GitHub\traffic-light-testing\task2> 