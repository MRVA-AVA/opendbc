from opendbc.car import structs, get_safety_config
from opendbc.car.interfaces import CarInterfaceBase

class CarInterface(CarInterfaceBase):

  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, experimental_long, docs) -> structs.CarParams:
    ret.brand = "mrva"
    ret.safetyConfigs = [get_safety_config(structs.CarParams.SafetyModel.ava)]

    # Needs safety validation and final testing before pulling out of dashcam
    ret.dashcamOnly = False

    ret.steerLimitTimer = 1.0
    ret.steerActuatorDelay = 0.25

    ret.steerControlType = structs.CarParams.SteerControlType.angle
    ret.radarUnavailable = True

    ret.openpilotLongitudinalControl = True

    return ret