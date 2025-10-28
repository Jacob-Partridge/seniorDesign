import time
from adafruit_servokit import ServoKit


def despenseSpice(servo: int):
    print("I worked")
    # Initialize the kit.
    kit = ServoKit(channels=16)

    # Access the continuous rotation servo property on channel 0
    continuous_servo = kit.continuous_servo[0]

    print("Controlling Continuous Rotation Servo on Channel 0...")

    # --- 1. STOP ---
    # Set the throttle to 0.0 (or close to it) to stop the servo.
    continuous_servo.throttle = 0.0
    print("Throttle: 0.0 (Stopped)")
    time.sleep(1)

    # --- 2. FORWARD ---
    # Set the throttle to a positive value (up to +1.0) to rotate forward.
    # +1.0 is full speed forward.
    continuous_servo.throttle = 0.5
    print("Throttle: 0.5 (Half Speed Forward)")
    time.sleep(5)

    # --- 3. REVERSE ---
    # Set the throttle to a negative value (down to -1.0) to rotate backward.
    # -1.0 is full speed reverse.
    continuous_servo.throttle = -0.5
    print("Throttle: -0.75 (3/4 Speed Reverse)")
    time.sleep(5)

    # --- 4. STOP AGAIN ---
    continuous_servo.throttle = 0.0
    print("Throttle: 0.0 (Stopped)")
    time.sleep(1)
    return