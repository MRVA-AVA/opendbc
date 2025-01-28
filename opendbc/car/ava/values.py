from dataclasses import dataclass, field
from opendbc.car import Platforms, PlatformConfig, DbcDict, Bus, CarSpecs

@dataclass
class AvaCarDocs:
  package: str = "All"

@dataclass
class AvaPlatformConfig(PlatformConfig):
  dbc_dict: DbcDict = field(default_factory=lambda: {Bus.pt: 'ava_pt'})

class CAR(Platforms):
  AVA = AvaPlatformConfig(
    [],
    CarSpecs(mass=1899., wheelbase=2.875, steerRatio=12.0),
  )

class CANBUS:
  vehicle = 0

DBC = CAR.create_dbc_map()