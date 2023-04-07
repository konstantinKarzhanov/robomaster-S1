# import the time module to sleep for some time later on "sleeping points"
import time

# A flag variable is defined for later use
flag = None

def scanForSign(scantype) :
# The function enables detection of markers using the vision system
    # Set the marker detection distance for the vision system to the given distance
    # vision_ctrl.set_marker_detection_distance(distance)
    # Enable detection of markers using the vision system
    if scantype == "person" :
        vision_ctrl.enable_detection(rm_define.vision_detection_people)
    elif scantype == "fire" :
        vision_ctrl.enable_detection(rm_define.vision_detection_marker)

    # Print a message to indicate that vision control has been enabled
    print("Vision control is enabled")


def vision_recognized_people(msg):
# Function that is called when person found is true
    # Change color to Deep Green
    # led_ctrl.set_top_led(rm_define.armor_all, 0 , 128, 0, rm_define.effect_always_on)
    # led_ctrl.set_bottom_led(rm_define.armor_all, 0, 128, 0, rm_define.effect_always_on)
    # Globalize ther person found variable to use it in this function
    global flag
    flag = True
    # Disabling the camera to prevent further person detections
    vision_ctrl.disable_detection(rm_define.vision_detection_people)
    # Play sound as audio cue person has been identified
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)
    

def vision_recognized_marker_letter_F(msg) :
# The function recognizes a specific marker (in this case, the letter "F") using the RoboMaster S1's vision system
    global flag
    flag = True
    # Detect and aim at the letter 'F' marker using the robot's vision system
    vision_ctrl.detect_marker_and_aim(rm_define.marker_letter_F)
    # Print a message indicating that the letter 'F' marker has been found
    print("I've found a letter 'F'")
    # Disable marker detection to avoid interference with other operations
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    # Print a message indicating that vision control has been disabled
    print("Vision control now disabled")

    # Fire the robot's blaster gun
    gun_ctrl.fire_once()


def readTheSign() :
# The function scans the environment for signs using the RoboMaster S1's gimbal
    global flag
    flag = False
    # a little bit up
    gimbal_ctrl.pitch_ctrl(15)

    while not flag :
    # Loop until flag is set to true
        # Move gimbal to the left by 45 degrees
        gimbal_ctrl.yaw_ctrl(-75)
        # Move gimbal to the right by 45 degrees
        gimbal_ctrl.yaw_ctrl(75)
    
    gimbal_ctrl.recenter()
    

def roomAction(number, roomtype) :
    if number == 1 :
        # MOVE TO THE ROOM
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.3) # move forward 2.3 meters

        if roomtype == "fire" or roomtype == "person" :
            # MOVE TO THE SIGN
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter() # recenter the gimbal

            chassis_ctrl.move_with_distance(0, 4.7) # move forward 4.7 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter() # recenter the gimbal

            # READ THE SIGN
            scanForSign(roomtype) # scan for marker or person
            readTheSign() # read the sign

            # EXIT THE ROOM
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter() # recenter the gimbal

            chassis_ctrl.move_with_distance(0, 4.7) # move forward 4.7 meters
            
            if roomtype == "fire" :
                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
                gimbal_ctrl.recenter() # recenter the gimbal
                time.sleep(3)
            elif roomtype == "person" :
                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
                gimbal_ctrl.recenter() # recenter the gimbal

                time.sleep(3)

                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 2.3) # move forward 2.3 meters

                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180) # rotate 180 degrees clockwise
                gimbal_ctrl.recenter() # recenter the gimbal

                # MOVE BACK TO THE ROOM
                time.sleep(5)
                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 2.3) # move forward 2.3 meters

        elif roomtype == "poison" :
            # MOVE TO THE SIGN
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter() # recenter the gimbal

            # READ THE SIGN
            for i in range(3) :
                gimbal_ctrl.yaw_ctrl(-15)
                gimbal_ctrl.yaw_ctrl(15)

            gimbal_ctrl.recenter() # recenter the gimbal

            # EXIT THE ROOM
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter() # recenter the gimbal

    if number == 2 and roomtype == "poison" :
        # MOVE TO THE ROOM
        # Move the robot to room Two by calling several movement commands to move forward, rotate, and move again
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # rotate 45 degrees anticlockwise
        gimbal_ctrl.recenter()

        chassis_ctrl.move_with_distance(0, 2.7) # move forward 2.7 meters
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # rotate 45 degrees anticlockwise
        gimbal_ctrl.recenter()

        # Re-adjusting point, sleep for 5 seconds
        time.sleep(5)

        # Continue to move forward and reach room Two 
        chassis_ctrl.move_with_distance(0, 2.5) # move forward 2.5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

        # MOVE TO THE SIGN
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
        gimbal_ctrl.recenter() # recenter the gimbal

        # READ THE SIGN
        for i in range(3) :
            gimbal_ctrl.yaw_ctrl(-15)
            gimbal_ctrl.yaw_ctrl(15)

        gimbal_ctrl.recenter() # recenter the gimbal

        # EXIT THE ROOM
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
        gimbal_ctrl.recenter()

    if number == 3 :
        # MOVE TO THE ROOM
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 4) # move forward 4 meters

        if roomtype == "fire" or roomtype == "person" :
            # MOVE TO THE SIGN
            # If the roomNumber is 3, move through a series of movements to reach the destination
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.96) # move forward 1.96 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.6) # move forward 1.6 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 4.9) # move forward 4.85 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.4) # move forward 1.4 meters

            # READ THE SIGN
            scanForSign(roomtype) # scan for marker or person
            readTheSign() # read the sign

            # EXIT THE ROOM
            # If the roomNumber is 3, move through a series of movements to exit the room
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180) # rotate 180 degrees clockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.4) # move forward 1.4 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter()
            
            chassis_ctrl.move_with_distance(0, 4.9) # move forward 4.85 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.6) # move forward 1.6 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 1.96) # move forward 1.96 meters

            if roomtype == "fire" :
                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
                gimbal_ctrl.recenter()
            elif roomtype == "person" :
                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees anticlockwise
                gimbal_ctrl.recenter()

                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 4) # move forward 4 meters

                chassis_ctrl.move_with_distance(0, 2.5) # move forward 2.5 meters
                chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise
                gimbal_ctrl.recenter()

                chassis_ctrl.move_with_distance(0, 2.7) # move forward 2.7 meters
                chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise
                gimbal_ctrl.recenter()

                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 2.3) # move forward 2.3 meters

                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180) # rotate 90 degrees anticlockwise
                gimbal_ctrl.recenter() # recenter the gimbal

                # MOVE BACK TO THE ROOM
                time.sleep(5)

                # MOVE TO THE FIRST ROOM
                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 2.3) # move forward 2.3 meters

                # MOVE TO THE SECOND ROOM
                # Move the robot to room Two by calling several movement commands to move forward, rotate, and move again
                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # rotate 45 degrees anticlockwise
                gimbal_ctrl.recenter()

                chassis_ctrl.move_with_distance(0, 2.7) # move forward 2.7 meters
                chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 45) # rotate 45 degrees anticlockwise
                gimbal_ctrl.recenter()

                # Re-adjusting point, sleep for 5 seconds
                time.sleep(5)

                # Continue to move forward and reach room Two 
                chassis_ctrl.move_with_distance(0, 2.5) # move forward 2.5 meters
                chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

                # MOVE TO THE THIRD ROOM
                chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
                chassis_ctrl.move_with_distance(0, 4) # move forward 4 meters

        elif roomtype == "poison" :
            # MOVE TO THE SIGN
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter() # recenter the gimbal

            # READ THE SIGN
            for i in range(3) :
                gimbal_ctrl.yaw_ctrl(-15)
                gimbal_ctrl.yaw_ctrl(15)

            gimbal_ctrl.recenter() # recenter the gimbal

            # EXIT THE ROOM
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

    if number == 4 :
        # MOVE TO THE ROOM
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 0.3) # move forward 0.3 meters

        if roomtype == "fire" or roomtype == "person" :
            # MOVE TO THE SIGN
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

            # READ THE SIGN
            scanForSign(roomtype) # scan for marker or person
            readTheSign() # read the sign

            # EXIT THE ROOM
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter()

            chassis_ctrl.move_with_distance(0, 2.1) # move forward 2.1 meters
            chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

        elif roomtype == "poison" :
            # MOVE TO THE SIGN
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees anticlockwise
            gimbal_ctrl.recenter() # recenter the gimbal

            # READ THE SIGN
            for i in range(3) :
                gimbal_ctrl.yaw_ctrl(-15)
                gimbal_ctrl.yaw_ctrl(15)

            gimbal_ctrl.recenter() # recenter the gimbal

            # EXIT THE ROOM
            chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90) # rotate 90 degrees clockwise
            gimbal_ctrl.recenter()

        # GO TO STARTING POINT
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 0.3) # move forward 0.3 meters

        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 4) # move forward 4 meters

        chassis_ctrl.move_with_distance(0, 2.5) # move forward 2.5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise
        gimbal_ctrl.recenter()

        chassis_ctrl.move_with_distance(0, 2.7) # move forward 2.7 meters
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45) # rotate 45 degrees anticlockwise
        gimbal_ctrl.recenter()

        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.6) # move forward 2.6 meters

        chassis_ctrl.move_with_distance(0, 5) # move forward 5 meters
        chassis_ctrl.move_with_distance(0, 2.3) # move forward 2.3 meters

        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180) # rotate 90 degrees anticlockwise
        gimbal_ctrl.recenter() # recenter the gimbal



def start() :
    global flag
    # Set robot mode to free mode
    robot_ctrl.set_mode(rm_define.robot_mode_free)

    # Set chassis and gimbal movement speeds
    chassis_ctrl.set_trans_speed(.5)
    gimbal_ctrl.set_rotate_speed(60)
    chassis_ctrl.set_rotate_speed(.7)

    # roomAction(1, "person")
    # roomAction(1, "fire")
    # roomAction(1, "poison")
    # roomAction(2, "poison")
    # roomAction(3, "person")
    roomAction(4, "person")

