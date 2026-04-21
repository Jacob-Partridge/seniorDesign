from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
channel = 0
userInput = ''
turnServo = kit.continuous_servo[channel]

while userInput != 'exit':
    userInput = input("-1 to 1")
    turnServo.throttle = float(userInput)

turnServo.throttle = 0
