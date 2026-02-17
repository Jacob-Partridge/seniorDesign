import time
from adafruit_servokit import ServoKit

while input != "Done" and input != "done":
    kit = ServoKit(channels=16)
    continuous_servo = kit.continuous_servo[0]
    print("Enter the time you want to run the servo for (in seconds) or type 'Done' to stop:")
    user_input = input()
    continuous_servo.throttle = 0.2
    time.sleep(float(user_input))
    continuous_servo.throttle = 0
