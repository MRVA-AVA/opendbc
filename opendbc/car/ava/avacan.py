from opendbc.car.ava.values import DriveMode, CANBUS, ControlRange
import numpy as np

class AvaCan:
  def __init__(self, packer):
    self.packer = packer
    self.counter = np.uint8(0)

  def create_auto_command(self, throttle: float, brake: float, steer: float):
    # This function creates a CAN message to control the vehicle
    # Expected inputs:
    # throttle: float, range [0, 100] %
    # brake: float, range [0, 600] psi
    # steer: float, range [-12.5, 12.5] degrees

    throttle = np.clip(throttle, ControlRange.MIN_THROTTLE, ControlRange.MAX_THROTTLE)
    brake = np.clip(brake, ControlRange.MIN_BRAKE, ControlRange.MAX_BRAKE)
    steer = np.clip(steer, ControlRange.MIN_STEER, ControlRange.MAX_STEER)

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

def create_autonomous_auto_command(self, left_turn_signal: bool, right_turn_signal: bool, low_beam: bool, high_beam: bool, running_lights: bool, horn: bool)
    # This function creates a CAN message to switches on the vehicle
    # Expected inputs:
    # left_turn_signal: bool, True if left turn signal is on
    # right_turn_signal: bool, True if right turn signal is on
    # low_beam: bool, True if low beam is on
    # high_beam: bool, True if high beam is on
    # running_lights: bool, True if running lights are on
    # horn: bool, True if horn is on

    values = {
      "Left_Turn_Signal": left_turn_signal,
      "Right_Turn_Signal": right_turn_signal,
      "Low_Beam": low_beam,
      "High_Beam": high_beam,
      "Running_Lights": running_lights,
      "Horn": horn,
    }

    return self.packer.make_can_msg("AutonomousAutoFunctions", CANBUS.vehicle, values)