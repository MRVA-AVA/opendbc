from dataclasses import dataclass, field
from opendbc.car import Platforms, PlatformConfig, DbcDict, Bus, CarSpecs
from opendbc.car.structs import CarState
from enum import IntEnum

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
    [],
    CarSpecs(mass=1899., wheelbase=2.875, steerRatio=12.0),
  )

class CANBUS:
  vehicle = 0

DBC = CAR.create_dbc_map()