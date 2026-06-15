from config import MAX_STEER
from pybricks.ev3devices import GyroSensor, Motor
from pybricks.tools import StopWatch
from utils import constrain, normalize_angle

Kp = 0.4
Ki = 0
Kd = 0.1


class Steering:
    def __init__(self, motor: Motor, gyro: GyroSensor):
        self.motor = motor
        self.gyro = gyro
        self.target_angle = 0
        self.integral_sum = 0
        self.last_error = 0
        self.timer = StopWatch()
        self.last_time = 0
        self.heading = 0

    def increase_target_angle(self, angle):
        self.target_angle += angle

    def reset_angles(self):
        self.motor.run_until_stalled(-500)
        self.motor.reset_angle(0)
        self.motor.run_until_stalled(500)
        angle = self.motor.angle()
        self.motor.run_angle(-500, angle // 2)

        self.motor.reset_angle(0)
        self.gyro.reset_angle(0)

    def pid(self, pixy=0.0, wall=0.0):
        current_time = self.timer.time() / 1000
        dt = current_time - self.last_time
        self.last_time = current_time
        dt = max(dt, 0.01)

        self.heading = self.gyro.angle()

        error = self.target_angle - self.heading

        if abs(error) < 2:
            error = 0

        derivative = (error - self.last_error) / dt
        self.integral_sum += error * dt

        self.integral_sum = constrain(self.integral_sum, -100, 100)  # TODO: CHANGE IT

        out = (error * Kp) + (self.integral_sum * Ki) + (derivative * Kd)

        out += wall
        if abs(pixy) > 0:
            out = pixy

        out = constrain(out, -MAX_STEER, MAX_STEER)

        self.motor.track_target(out)

        self.last_error = error

        return out
