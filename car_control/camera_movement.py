import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class StepperMotor:
    STEP_SEQUENCE = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
    ]
    PROCESSING_DELAY = 0.001

    def __init__(self, in1, in2, in3, in4):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.direction = None

        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

    def set_step(self, w1, w2, w3, w4):
        GPIO.output(self.IN1, w1)
        GPIO.output(self.IN2, w2)
        GPIO.output(self.IN3, w3)
        GPIO.output(self.IN4, w4)

    def rotate(self, direction):
        if direction not in {"left", "right"}:
            raise ValueError("Invalid direction. Use 'left' or 'right'.")

        self.direction = direction

        steps = (
            StepperMotor.STEP_SEQUENCE[:]
            if self.direction == "right"
            else StepperMotor.STEP_SEQUENCE[::-1]
        )
        while self.direction == direction:
            for step in steps:
                self.set_step(*step)
                time.sleep(StepperMotor.PROCESSING_DELAY)

    def stop(self):
        self.set_step(0, 0, 0, 0)
        self.direction = None


panning_motor = StepperMotor(6, 13, 19, 26)


def pan_camera(direction):
    if direction not in {"left", "right", "stop"}:
        raise ValueError("Invalid direction. Use 'left', 'right', or 'stop'.")

    if direction == "stop":
        panning_motor.stop()
    else:
        panning_motor.rotate(direction)
