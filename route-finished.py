# import the time module to sleep for some time later on our "sleeping points"
import time
import random


def random_int(low_value, high_value) :
    return random.randint(low_value, high_value)
    

def led_flash(r,g,b):
# The function sets the bottom and top LEDs of the robot to the specified color and flashes them
# r, g, b: integer values between 0 and 255 representing the amount of red, green and blue colors respectively
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, r, g, b, rm_define.effect_flash)
    led_ctrl.set_top_led(rm_define.armor_top_all, r, g, b, rm_define.effect_flash)


def led_solid(r,g,b):
# The function sets the bottom and top LEDs of the robot to the specified solid color
# r, g, b: integer values between 0 and 255 representing the amount of red, green and blue colors respectively
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, r, g, b, rm_define.effect_always_on)
    led_ctrl.set_top_led(rm_define.armor_top_all, r, g, b, rm_define.effect_always_on)


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
    led_ctrl.gun_led_on()
    gun_ctrl.fire_once()
    led_ctrl.gun_led_off()


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


def scenario_sleep(time_in_seconds, r = 0, g = 0, b = 139) :
    # Set LED to Dark Blue (by default) - Sleep
    led_solid(r, g, b)
    time.sleep(time_in_seconds)


def route_section_one(route_type) :
# The function moves the robot along the first section

    if route_type == "forward":
        # Set LEDs Flashing Purple - Indicating Movement
        led_flash(138, 43, 226)
    elif route_type == "backward":
        # Set LEDs Flashing Green - Indicating Movement to Safety
        led_flash(0, 255, 0)

    # Robot Movement
    chassis_ctrl.move_with_distance(0, 5) # Move  robot forward 5 meters
    chassis_ctrl.move_with_distance(0, 2.3) # Move robot forward 2.3 meters


def route_section_two(route_type) :
# The function moves the robot along the second section
    if route_type == "forward" :
        # Set LEDs to Flash Purple - Indicate Movement
        led_flash(139, 0, 139)

        # Robot Movement
        chassis_ctrl.move_with_distance(0, 5) # Move robot forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # Move robot forward 2.6 meters
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # Rotate robot 45 degrees anticlockwise

        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        # Robot Movement
        chassis_ctrl.move_with_distance(0, 2.7) # Move forward 2.7 meters
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # Rotate 45 degrees anticlockwise

        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        # Sleeping point to adjust the angle of movement
        scenario_sleep(5)

        # Set LEDs to Flash Purple - Indicate Movement
        led_flash(139, 0, 139)
        chassis_ctrl.move_with_distance(0, 2.5) # Move robot forward 2.5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # Move robot forward 2.6 meters


    elif route_type == "backward" :
        # Set LEDs to Flash Green - Return Person to Safety
        led_flash(0, 255, 0)

        # Robot Movement
        chassis_ctrl.move_with_distance(0, 2.5) # move forward 2.5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise

        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        # Robot Movement
        chassis_ctrl.move_with_distance(0, 2.7) # move forward 2.7 meters
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise

        # Recenter the gimbal to its default position
        gimbal_ctrl.recenter()

        # Sleeping point to adjust the angle of movement
        scenario_sleep(5)

        # Set LEDs to Flash Green - Return Person to Safety
        led_flash(0, 255, 0)

        # Robot Movement 
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meterS
        

def route_section_three(route_type) :
# The function moves the robot along the third section

    if route_type == "forward":
        # Set LEDs to Flashing Purple - Indicating Movement
        led_flash(139, 0, 139)
    elif route_type == "backward":
        # Set LEDs to Flash Green - Move Person to Safety
        led_flash(0, 255, 0)

    # Robot Movement
    chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
    chassis_ctrl.move_with_distance(0, 4) # move forward 4 meters


def route_section_four(route_type) :
# The function moves the robot along the fourth section

    if route_type == "forward":
        # Set LEDs to Flash Purple - Indicate Movement
        led_flash(139, 0, 139)
    elif route_type == "backward":
        # Set LEDs to Flash Green - Move Person to Safety
        led_flash(0, 255, 0)

    # Robot Movement
    chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
    chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
    chassis_ctrl.move_with_distance(0, 0.3) # move forward 0.3 meters


def rotate_starting_point() :
    # Set LEDs to Flash Purple - Indicate Movement
    led_flash(139, 0, 139)

    # Robot Movement
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180) # rotate 180 degrees anticlockwise

    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()


def scenario_danger(route_type) :
# The function controls the movement and actions of a robot for a "danger" scenario
    
    # Set LEDs to Flash Red - Indicate Danger
    led_flash(255, 0, 0)

    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()

    # Simulate shaking head (left to right)
    for i in range(2) :
        gimbal_ctrl.yaw_ctrl(-15)
        gimbal_ctrl.yaw_ctrl(15)

    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()

    if route_type == "forward" :
        # Leave the room based on scenario

        # Set LEDs to Flash Purple - Indicate Movement
        led_flash(139, 0, 139)

        # Robot Movement
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise


    elif route_type == "backward" :
        # Leave the room based on scenario

        # Set LEDs to Flash Green - Move Person to Safety
        led_flash(0, 255, 0)

        # Robot Movement
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees clockwise

    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()


def scenario_disco(dance_num = 2, dance_dist = .2, low_degree = 0, high_degree = 360, low_color = 0, high_color = 255, pitch_low = -20, pitch_high = 35, yaw_low = 0, yaw_high = 250, speed_low = 300, speed_high = 540, f_freq_low = 2, f_freq_high = 10, error_low = 1, error_high = 30) :
# This function generates random movements and colors for the robot to perform a disco dance
# It takes in several parameters that determine the range of values for various aspects of the dance

    # List of choices for the robot's chassis rotation direction
    list_chassis_choices = [rm_define.clockwise, rm_define.anticlockwise]

    # Loop to perform the dance moves number of times
    for i in range(dance_num) :
        # Set random speeds for the gimbal and chassis rotation
        gimbal_ctrl.set_rotate_speed(random_int(speed_low, speed_high))
        chassis_ctrl.set_rotate_speed(random_int(speed_low, speed_high))

        # Flash the LEDs with a random frequency and color
        led_ctrl.set_flash(rm_define.armor_all, random_int(f_freq_low, f_freq_high))
        led_flash(random_int(low_color, high_color),random_int(low_color, high_color),random_int(low_color, high_color))
        
        # Alternate between moving the chassis left and right while the LEDs on
        if i % 2 == 0 :
            chassis_ctrl.move_with_distance(-90, dance_dist)
        elif i % 2 != 0 :
            chassis_ctrl.move_with_distance(90, dance_dist)


        # Rotate the chassis in a random direction
        chassis_ctrl.rotate_with_degree(random.choice(list_chassis_choices), random_int(low_degree, high_degree))
        
        # Pitch in a random direction
        gimbal_ctrl.pitch_ctrl(random_int(pitch_low, pitch_high))

        # Yaw in a random direction
        gimbal_ctrl.yaw_ctrl(random_int(yaw_low, yaw_high))

        # Print a string of "ERROR!!!" with random repetition to create noise
        print(" ERROR!!! " * random_int(error_low, error_high))

        # Pause briefly before the next iteration of the loop
        # time.sleep(.2)

    # Recenter the gimbal to its default position
    gimbal_ctrl.recenter()


def act_by_scenario(room_number, room_type) :
# The function controls the movement and actions of a robot in different scenarios depending on the "room_number" and "room_type" parameters
    if room_number == 1 :
        # Come up to the rooms door
        route_section_one("forward")

        if room_type == "marker" or room_type == "people" :
        # Set LEDs to Flashing Red - Danger
            led_flash(255, 0, 0)

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
                #  Set LEDs Flashing Purple - Indicate Movement
                led_flash(130, 0, 139)
                # Robot Movement
                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()
                

            elif room_type == "people":
                # Set LEDs to Flashing Green - Move Person to Safety
                led_flash(0, 255, 0)

                # Robot Movement
                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise

                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()
                
                # Return to the starting point
                route_section_one("backward")
                rotate_starting_point()

                # Sleeping point to adjust the angle of movement
                scenario_sleep(5)

                # Come up to the rooms door
                route_section_one("forward")

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
        route_section_three("forward")

        if room_type == "marker" or room_type == "people" :
            # Set LEDs to Flashing Red - Danger
            led_flash(255, 0, 0)

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

            # Robot Movement
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
                # Set LEDs to Flashing Purple
                led_flash(139, 0, 139)

                # Robot Movement
                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()

            elif room_type == "people" :
                # Set LEDs to Flashing Green to Safety
                led_flash(0, 255, 0)

                # Robot Movement
                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees anticlockwise
                # Recenter the gimbal to its default position
                gimbal_ctrl.recenter()

                # Return to the starting point
                route_section_three("backward")
                route_section_two("backward")
                route_section_one("backward")
                rotate_starting_point()

                # Sleeping point to adjust the angle of movement
                scenario_sleep(5)

                # Come up to the rooms door
                route_section_one("forward")
                route_section_two("forward")
                route_section_three("forward")

        elif room_type == "danger" :
        # Act according to the "danger" scenario
            scenario_danger("forward")

    if room_number == 4 :
        # Come up to the rooms door
        route_section_four("forward")

        if room_type == "marker" or room_type == "people" :
            # Set LEDs Flashing Red - Indicate Danger
            led_flash(255, 0 ,0)
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
        scenario_sleep(5)

        # Return to the starting point
        route_section_four("backward")
        route_section_three("backward")
        route_section_two("backward")
        route_section_one("backward")
        rotate_starting_point()


def start() :
    global flag
    # Set robot mode to free mode
    robot_ctrl.set_mode(rm_define.robot_mode_free)

    # Set number of shots per time
    gun_ctrl.set_fire_count(3)

    # Set chassis and gimbal movement speeds
    gimbal_ctrl.set_rotate_speed(60)
    chassis_ctrl.set_trans_speed(.6)
    chassis_ctrl.set_rotate_speed(60)

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
    # act_by_scenario(4, "people"

    # ----------------------------
    # Sprint Scenario starts here
    # ----------------------------

    # act_by_scenario(1, "people")
    # act_by_scenario(2, "danger")
    # act_by_scenario(3, "marker")
    # act_by_scenario(4, "marker")
    scenario_disco(10)
    


