from dataclasses import dataclass, field
from opendbc.car import Platforms, PlatformConfig, DbcDict, Bus, CarSpecs
from opendbc.car.structs import CarState
from enum import IntEnum

@dataclass
class ControlRange:
  MIN_THROTTLE: float = 0.0
  MAX_THROTTLE: float = 100.0
  MIN_BRAKE: float = 0.0
  MAX_BRAKE: float = 600.0
  MIN_STEER: float = -12.5
  MAX_STEER: float = 12.5

@dataclass
class AvaCarDocs:
  package: str = "All"

@dataclass
class AvaPlatformConfig(PlatformConfig):
  dbc_dict: DbcDict = field(default_factory=lambda: {Bus.pt: 'ava_pt'})

class DriveMode(IntEnum):
  FORWARD_DRIVE = 1
  REVERSE_DRIVE = 2
  PARK = 3
  NEUTRAL = 4

class CAR(Platforms):
  AVA_PT = AvaPlatformConfig(
    [AvaCarDocs("Ava PT")],
    CarSpecs(mass=818., wheelbase=2.4, steerRatio=12.0),
  )

class CANBUS:
  vehicle = 0

DBC = CAR.create_dbc_map()