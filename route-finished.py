# import the time module to sleep for some time later on our "sleeping points"
import time

# The "flag" will be used later in the "scan_the_room" function to stop the endless loop when looking for a people or an "F" sign in a room.
flag = None

def enable_detection(detection_type) :
# The function enables detection of markers using the vision system
    if detection_type == "people" :
    # Enable detection of people using the vision system
        vision_ctrl.enable_detection(rm_define.vision_detection_people)
    elif detection_type == "marker" :
    # Enable detection of markers using the vision system
        vision_ctrl.enable_detection(rm_define.vision_detection_marker)

    # Print a message to indicate that vision control has been enabled
    print("Vision control has been enabled")


def vision_recognized_people(msg):
# The function that is automatically called by the "enable_detection" function when people are detected in the room
    global flag
    flag = True

    # Disable people detection to avoid interference with other operations
    vision_ctrl.disable_detection(rm_define.vision_detection_people)
    # Print a message indicating that vision control has been disabled
    print("Vision control has been disabled")

    # Play sound when people has been identified
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    

def vision_recognized_marker_letter_F(msg) :
# The function that is automatically called by the "enable_detection" function when marker (in this case, the letter "F") are detected in the room
    global flag
    flag = True

    # Detect and aim at the letter 'F' marker using the robot's vision system
    vision_ctrl.detect_marker_and_aim(rm_define.marker_letter_F)
    # Print a message indicating that the 'F' marker has been found
    print("The 'F' marker has been found")

    # Disable marker detection to avoid interference with other operations
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    # Print a message indicating that vision control has been disabled
    print("Vision control has been disabled")

    # Fire the robot's blaster gun
    gun_ctrl.fire_once()


def scan_the_room() :
# The function scans the environment using the enabled vision system (by function "enable_detection")
    global flag
    flag = False

    # Set the pitch angle of the gimbal to 20 degrees
    gimbal_ctrl.pitch_ctrl(20)

    while not flag :
    # Scan the room until the object is detected
        # Move gimbal to the left by 75 degrees
        gimbal_ctrl.yaw_ctrl(-75)
        # Move gimbal to the right by 75 degrees
        gimbal_ctrl.yaw_ctrl(75)
    
    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()


def route_section_one() :
# The function moves the robot along the first section
    chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
    chassis_ctrl.move_with_distance(0, 2.3) # move forward 2.3 meters


def route_section_two(route_mode) :
# The function moves the robot along the second section
    if route_mode == "forward" :
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # rotate 45 degrees anticlockwise
        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        chassis_ctrl.move_with_distance(0, 2.7) # move forward 2.7 meters
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # rotate 45 degrees anticlockwise
        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        # Sleeping point to adjust the angle of movement
        time.sleep(5)

        chassis_ctrl.move_with_distance(0, 2.5) # move forward 2.5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

    elif route_mode == "backward" :
        chassis_ctrl.move_with_distance(0, 2.5) # move forward 2.5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise
        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        chassis_ctrl.move_with_distance(0, 2.7) # move forward 2.7 meters
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise
        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        # Sleeping point to adjust the angle of movement
        time.sleep(5)

        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters


def route_section_three() :
# The function moves the robot along the third section
    chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
    chassis_ctrl.move_with_distance(0, 4) # move forward 4 meters


def route_section_four() :
# The function moves the robot along the fourth section
    chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
    chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
    chassis_ctrl.move_with_distance(0, 0.3) # move forward 0.3 meters


def rotate_starting_point() :
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180) # rotate 180 degrees anticlockwise
    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()


def scenario_danger(route_mode) :
# The function controls the movement and actions of a robot for a "danger" scenario
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()

    # Simulate shaking head (left to right)
    for i in range(2) :
        gimbal_ctrl.yaw_ctrl(-15)
        gimbal_ctrl.yaw_ctrl(15)

    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()

    if route_mode == "forward" :
        # Leave the room based on scenario
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise

    elif route_mode == "backward" :
        # Leave the room based on scenario
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees clockwise

    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()


def act_by_scenario(room_number, room_type) :
# The function controls the movement and actions of a robot in different scenarios depending on the "room_number" and "room_type" parameters
    if room_number == 1 :
        # Come up to the rooms door
        route_section_one()

        if room_type == "marker" or room_type == "people" :
        # Come up to the marker or the people inside the room
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 4.7) # move forward 4.7 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            # Detect the marker or people
            enable_detection(room_type) # enable vision system
            scan_the_room() # scan the environment

            # Leave the room based on scenario
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()
            chassis_ctrl.move_with_distance(0, 4.7) # move forward 4.7 meters
            
            if room_type == "marker" :
                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()
                
                # Sleeping point to adjust the angle of movement
                time.sleep(5)

            elif room_type == "people" :
                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()

                # Sleeping point to adjust the angle of movement
                time.sleep(5)
                
                # Return to the starting point
                route_section_one()
                rotate_starting_point()

                # Sleeping point to adjust the angle of movement
                time.sleep(5)

                # Come up to the rooms door
                route_section_one()

        elif room_type == "danger" :
        # Act according to the "danger" scenario
            scenario_danger("forward")

    if room_number == 2 and room_type == "danger" :
        # Come up to the rooms door
        route_section_two("forward")

        # Act according to the "danger" scenario
        scenario_danger("forward")

    if room_number == 3 :
        # Come up to the rooms door
        route_section_three()

        if room_type == "marker" or room_type == "people" :
            # Come up to the marker or the people inside the room
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.96) # move forward 1.96 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.6) # move forward 1.6 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 4.9) # move forward 4.9 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.4) # move forward 1.4 meters

            # Detect the marker or people
            enable_detection(room_type) # enable vision system
            scan_the_room() # scan the environment

            # Leave the room based on scenario
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180) # rotate 180 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.4) # move forward 1.4 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()
            
            chassis_ctrl.move_with_distance(0, 4.9) # move forward 4.9 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.6) # move forward 1.6 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.96) # move forward 1.96 meters

            if room_type == "marker" :
                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()

            elif room_type == "people" :
                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees anticlockwise
                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()

                # Return to the starting point
                route_section_three()
                route_section_two("backward")
                route_section_one()
                rotate_starting_point()

                # Sleeping point to adjust the angle of movement
                time.sleep(5)

                # Come up to the rooms door
                route_section_one()
                route_section_two("forward")
                route_section_three()

        elif room_type == "danger" :
        # Act according to the "danger" scenario
            scenario_danger("forward")

    if room_number == 4 :
        # Come up to the rooms door
        route_section_four()

        if room_type == "marker" or room_type == "people" :
            # Come up to the marker or the people inside the room
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            # Detect the marker or people
            enable_detection(room_type) # enable vision system
            scan_the_room() # scan the environment

            # Leave the room based on scenario
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            # Recenter the gimbal to its default position
            gimbal_ctrl.recenter()

        elif room_type == "danger" :
        # Act according to the "danger" scenario
            scenario_danger("backward")

        # Sleeping point to adjust the angle of movement
        time.sleep(5)

        # Return to the starting point
        route_section_four()
        route_section_three()
        route_section_two("backward")
        route_section_one()
        rotate_starting_point()


def start() :
    global flag
    # Set robot mode to free mode
    robot_ctrl.set_mode(rm_define.robot_mode_free)

    # Set chassis and gimbal movement speeds
    gimbal_ctrl.set_rotate_speed(60)
    chassis_ctrl.set_trans_speed(.5)
    chassis_ctrl.set_rotate_speed(.7)

    # The program was tested with these scenarios
    
    # Room One
    # act_by_scenario(1, "people")
    # act_by_scenario(1, "marker")
    # act_by_scenario(1, "danger")

    # Room Two
    # act_by_scenario(2, "danger")

    # Room Three
    # act_by_scenario(3, "people")

    # Room Four
    # act_by_scenario(4, "people")

