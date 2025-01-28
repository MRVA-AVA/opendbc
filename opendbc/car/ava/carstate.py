from opendbc.car.interfaces import CarStateBase
from opendbc.car import structs
from opendbc.can.parser import CANParser
from opendbc.car import Bus
from opendbc.car.ava.values import DBC, CANBUS

class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

  def update(self, can_parsers) -> structs.CarState:
    pass

  @staticmethod
  def get_can_parsers(CP):
    pt_messages = [
      ("AutonomousControls", 301),
    ]

    # Example: Bus.party: CANParser(DBC[CP.carFingerprint][Bus.party], party_messages, CANBUS.party),
    return {
      Bus.pt: CANParser(DBC[CP.carFingerprint][Bus.pt], pt_messages, CANBUS.vehicle),
    }