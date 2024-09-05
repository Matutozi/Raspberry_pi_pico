class Servos:
    def __init__(self, pin):
        import machine
        self.servoPin = pin
        self.obj = machine.PWM(machine.Pin(self.servoPin))
        self.obj.freq(50)

    def pos(self, angle):
        writeVal = 6553/180 * angle + 1638
        self.obj.duty_u16(int(writeVal))