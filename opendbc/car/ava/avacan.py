from opendbc.car.ava.values import DriveMode, CANBUS, ControlRange
import numpy as np

class AvaCan:
  def __init__(self, packer):
    self.packer = packer
    self.counter = np.uint8(0)

  def create_auto_command(self, throttle: float, brake: float, steer: float):
    throttle = np.clip(throttle, 0.0, 1.0) * ControlRange.MAX_THROTTLE
    brake = np.clip(brake, 0.0, 1.0) * ControlRange.MAX_BRAKE
    steer = 2.0 * np.clip(steer - 0.5, -0.5, 0.5) * ControlRange.MAX_STEER

    throttle = 0.0 if brake > 0.0 else throttle

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

def create_autonomous_auto_command(self, left_turn_signal: bool, right_turn_signal: bool, low_beam: bool, high_beam: bool, running_lights: bool, horn: bool):
    values = {
      "Left_Turn_Signal": left_turn_signal,
      "Right_Turn_Signal": right_turn_signal,
      "Low_Beam": low_beam,
      "High_Beam": high_beam,
      "Running_Lights": running_lights,
      "Horn": horn,
    }

    return self.packer.make_can_msg("AutonomousAutoFunctions", CANBUS.vehicle, values)