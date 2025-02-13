from opendbc.car.interfaces import CarStateBase
from opendbc.car import structs
from opendbc.can.parser import CANParser
from opendbc.car import Bus
from opendbc.car.ava.values import DBC, CANBUS, DriveMode
from opendbc.car.common.conversions import Conversions as CV

class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

  def update(self, can_parsers) -> structs.CarState:
    cp = can_parsers[Bus.pt]

    ret = structs.CarState()

    # Vehicle speed
    ret.vEgoRaw = cp.vl["AutonomousFeedbackDynamics"]["WheelSpeed"] * CV.MPH_TO_MS
    ret.vEgo, ret.aEgo = self.update_speed_kf(ret.vEgoRaw)

    # Gas pedal
    ret.gasPressed = bool(cp.vl["AutonomousFeedbackStates"]["GasPressed"])

    # Brake pedal
    ret.brakePressed = bool(cp.vl["AutonomousFeedbackStates"]["BrakePressed"])

    # Steering wheel
    ret.steeringAngleDeg = cp.vl["AutonomousFeedbackControls"]["SteeringAngleDeg"]
    ret.steeringPressed = bool(cp.vl["AutonomousFeedbackStates"]["SteeringPressed"])

    ret.steerFaultTemporary = bool(cp.vl["AutonomousFeedbackStates"]["SteerFaultTemporary"])
    ret.steerFaultPermanent = bool(cp.vl["AutonomousFeedbackStates"]["SteerFaultPermanent"])

    # Cruise state
    ret.cruiseState.enabled = True
    ret.cruiseState.speed = 20.0
    ret.cruiseState.available = True
    ret.cruiseState.standstill = False
    ret.standstill = False
    ret.accFaulted = False

    # Doors
    ret.doorOpen = False

    # Blinker
    ret.leftBlinker = bool(cp.vl["AutonomousFeedbackStates"]["LeftBlinker"])
    ret.rightBlinker = bool(cp.vl["AutonomousFeedbackStates"]["RightBlinker"])

    # Seatbelt
    ret.seatbeltUnlatched = bool(cp.vl["AutonomousFeedbackStates"]["SeatBeltUnlatched"])

    # Blindspot
    ret.leftBlindspot = False
    ret.rightBlindspot = False

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

    # Example: Bus.party: CANParser(DBC[CP.carFingerprint][Bus.party], party_messages, CANBUS.party),
    return {
      Bus.pt: CANParser(DBC[CP.carFingerprint][Bus.pt], pt_messages, CANBUS.vehicle),
    }