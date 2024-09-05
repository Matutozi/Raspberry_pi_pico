from servos import Servos
from machine import Pin
import time

servoPin = 16
myServo = Servos(servoPin)

def test_servo():
    try:
        while True:
            for angle in range(0, 181, 30):
                print(f"Moving servo to {angle} degrees.")
                myServo.pos(angle)
                time.sleep(1)
                
            for angle in range(180, -1, -30):
                print(f"Moving servo to {angle} degrees.")
                myServo.pos(angle)
                time.sleep(1)
    except KeyboardInterrupt:
        myServo.pos(0)
        print("Program Terminated")

test_servo()
