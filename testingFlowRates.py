import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
continuous_servo = kit.continuous_servo[0]

while input != "Done" and input != "done":
    user_input = input()
    if user_input == "Done" or user_input == "done":
        break
    
    print("Enter the time you want to run the servo for (in seconds) or type 'Done' to stop:")
    continuous_servo.throttle = 0.2
    time.sleep(float(user_input))
    continuous_servo.throttle = 0
