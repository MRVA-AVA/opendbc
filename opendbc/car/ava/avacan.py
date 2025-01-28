from opendbc.car.ava.values import DriveMode, CANBUS
import numpy as np

class AvaCan:
  def __init__(self, packer):
    self.packer = packer
    self.counter = np.uint8(0)

  def create_auto_command(self, throttle, brake, steer):
    if (brake > 0.0):
      throttle = 0.0
    else:
      brake = 0.0

    values = {
      "SteeringAngleRequest": steer,
      "ThrottleRequest": throttle,
      "BrakeRequest": brake,
      "AutonomousSystemHeartbeat": self.counter,
      "AutonomousSystemReady": True,
      "AutonomousSystemEStop": False,
      "AutonomousSystemDirection": DriveMode.FORWARD_DRIVE,
    }

    self.counter += 1

    return self.packer.make_can_msg("AutonomousControls", CANBUS.vehicle, values)