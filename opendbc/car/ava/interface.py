from opendbc.car import structs, get_safety_config
from opendbc.car.interfaces import CarInterfaceBase

class CarInterface(CarInterfaceBase):
  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, experimental_long, docs) -> structs.CarParams:
    ret.brand = "ava"
    ret.steerControlType = structs.CarParams.SteerControlType.angle
    ret.transmissionType = structs.CarParams.TransmissionType.direct
    ret.dashcamOnly = False
    ret.radarUnavailable = True
    ret.openpilotLongitudinalControl = True
    ret.steerLimitTimer = 1.0

    ret.safetyConfigs = [get_safety_config(structs.CarParams.SafetyModel.ava)]

    return ret