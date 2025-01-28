from opendbc.car import structs
from opendbc.car.interfaces import CarInterfaceBase

class CarInterface(CarInterfaceBase):

  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, experimental_long, docs) -> structs.CarParams:
    ret.carName = "ava"

    # Needs safety validation and final testing before pulling out of dashcam
    ret.dashcamOnly = True

    ret.steerLimitTimer = 1.0
    ret.steerActuatorDelay = 0.25

    ret.steerControlType = structs.CarParams.SteerControlType.angle
    ret.radarUnavailable = True

    ret.openpilotLongitudinalControl = True

    return ret