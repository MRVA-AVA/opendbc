from dataclasses import dataclass, field
from opendbc.car import Platforms, PlatformConfig, DbcDict, Bus, CarSpecs
from enum import IntEnum
from opendbc.car.docs_definitions import CarDocs, CarParts, CarHarness

@dataclass
class ControlRange:
  MAX_THROTTLE: float = 100.0
  MAX_BRAKE: float = 600.0
  MAX_STEER: float = 20.0

@dataclass
class AvaCarDocs(CarDocs):
  package: str = "All"
  car_parts: CarParts = field(default_factory=CarParts.common([CarHarness.ava_pt]))

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