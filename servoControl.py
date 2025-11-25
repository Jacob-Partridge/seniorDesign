import time
from adafruit_servokit import ServoKit


def despenseSpice(servo: int):
    print("I worked")
    # Initialize the kit.
    kit = ServoKit(channels=16)

    # Access the continuous rotation servo property on channel 0
    continuous_servo = kit.continuous_servo[0]

    print("Controlling Continuous Rotation Servo on Channel 0...")

    # Set the throttle to 0.0 (or close to it) to stop the servo.
    continuous_servo.throttle = 0.0
    print("Throttle: 0.0 (Stopped)")
    time.sleep(1)

    # Set the throttle to a positive value to rotate forward.
    continuous_servo.throttle = 0.1
    print("Throttle: 0.5 (Half Speed Forward)")
    time.sleep(5)

    # Set the throttle to a negative value to rotate backward.
    continuous_servo.throttle = -0.1
    print("Throttle: -0.75 (3/4 Speed Reverse)")
    time.sleep(5)

    continuous_servo.throttle = 0.0
    print("Throttle: 0.0 (Stopped)")
    time.sleep(1)
    return