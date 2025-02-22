from opendbc.car.interfaces import CarStateBase
from opendbc.car import structs
from opendbc.car import Bus
from enum import StrEnum
from opendbc.can.parser import CANParser
from opendbc.car.common.conversions import Conversions as CV
from opendbc.car.ava.values import CANBUS, DBC

class CarState(CarStateBase):
  def __init__(self, CP: structs.CarParams):
    super().__init__(CP)

  def update(self, can_parsers: dict[StrEnum, CANParser]) -> structs.CarState:
    can_parser = can_parsers[Bus.pt]

    ret = structs.CarState()

    # Vehicle State
    ret.vEgoRaw = can_parser.vl["AutonomousFeedbackDynamics"]["WheelSpeed"] * CV.MPH_TO_MS
    ret.vEgo, ret.aEgo = self.update_speed_kf(ret.vEgoRaw)

    # Gas Pedal
    ret.gasPressed = bool(can_parser.vl["AutonomousFeedbackStates"]["GasPressed"])

    # Brake Pedal
    ret.brakePressed = bool(can_parser.vl["AutonomousFeedbackStates"]["BrakePressed"])

    # Steering wheel
    ret.steeringAngleDeg = can_parser.vl["AutonomousFeedbackControls"]["SteeringAngleDeg"]
    ret.steeringPressed = bool(can_parser.vl["AutonomousFeedbackStates"]["SteeringPressed"])

    ret.steerFaultTemporary = bool(can_parser.vl["AutonomousFeedbackStates"]["SteerFaultTemporary"])
    ret.steerFaultPermanent = bool(can_parser.vl["AutonomousFeedbackStates"]["SteerFaultPermanent"])

    # Blinker
    ret.leftBlinker = bool(can_parser.vl["AutonomousFeedbackStates"]["LeftBlinker"])
    ret.rightBlinker = bool(can_parser.vl["AutonomousFeedbackStates"]["RightBlinker"])

    return ret

  @staticmethod
  def get_can_parsers(CP):
    pt_messages = [
      # ("AutonomousAutoFunctions", 300),
      # ("AutonomousControls", 301),
      ("AutonomousFeedbackDynamics", 400),
      ("AutonomousFeedbackControls", 401),
      ("AutonomousFeedbackStates", 402),
    ]

    return {
      Bus.pt: CANParser(DBC[CP.carFingerprint][Bus.pt], pt_messages, CANBUS.vehicle),
    }