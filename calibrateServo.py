from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
channel = 0
input = ''
turnServo = kit.continuous_servo[channel]

while input != 'exit':
    input = input("-1 to 1")
    turnServo.throttle = float(input)

turnServo.throttle = 0
