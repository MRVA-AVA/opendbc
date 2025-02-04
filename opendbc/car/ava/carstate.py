from opendbc.car.interfaces import CarStateBase
from opendbc.car import structs
from opendbc.can.parser import CANParser
from opendbc.car import Bus
from opendbc.car.ava.values import DBC, CANBUS
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
    gas_pressed = cp.vl["AutonomousFeedbackStates"]["GasPressed"]
    ret.gasPressed = gas_pressed

    # Brake pedal
    ret.brakePressed = cp.vl["AutonomousFeedbackStates"]["BrakePressed"]

    # Steering wheel
    ret.steeringAngleDeg = cp.vl["AutonomousFeedbackControls"]["SteeringAngleDeg"]
    ret.steeringPressed = cp.vl["AutonomousFeedbackStates"]["SteeringPressed"]

    ret.steerFaultTemporary = cp.vl["AutonomousFeedbackStates"]["SteerFaultTemporary"]
    ret.steerFaultPermanent = cp.vl["AutonomousFeedbackStates"]["SteerFaultPermanent"]

    # Cruise state
    ret.cruiseState.enabled = True
    ret.cruiseState.speed = 20.0
    ret.cruiseState.available = True
    ret.cruiseState.standstill = False
    ret.standstill = False
    ret.accFaulted = False

    # Gear
    ret.gearShifter = CarState.GearShifter.drive

    # Doors
    ret.doorOpen = False

    # Blinker
    ret.leftBlinker = cp.vl["AutonomousFeedbackStates"]["LeftBlinker"]
    ret.rightBlinker = cp.vl["AutonomousFeedbackStates"]["RightBlinker"]

    # Seatbelt
    ret.seatbeltUnlatched = cp.vl["AutonomousFeedbackStates"]["SeatbeltUnlatched"]

    # Blindspot
    ret.leftBlindspot = False
    ret.rightBlindspot = False

    return ret

  @staticmethod
  def get_can_parsers(CP):
    pt_messages = [
      ("AutonomousControls", 301),
    ]

    # Example: Bus.party: CANParser(DBC[CP.carFingerprint][Bus.party], party_messages, CANBUS.party),
    return {
      Bus.pt: CANParser(DBC[CP.carFingerprint][Bus.pt], pt_messages, CANBUS.vehicle),
    }