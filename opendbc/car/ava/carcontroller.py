from opendbc.car.interfaces import CarControllerBase
from opendbc.can.packer import CANPacker
from opendbc.car import Bus, structs
from opendbc.car.ava.avacan import AvaCan
from enum import StrEnum

class CarController(CarControllerBase):
  def __init__(self, dbc_names: dict[StrEnum, str], CP: structs.CarParams):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.pt])
    self.ava_can = AvaCan(self.packer)

  def update(self, CC, CS, now_nanos):
    actuators = CC.actuators

    throttle = actuators.accel if actuators.accel > 0.0 else 0.0
    brake = abs(actuators.accel) if actuators.accel < 0.0 else 0.0
    steer = actuators.steeringAngleDeg

    # TODO (moises): Find vehicle model to convert from acceleration to throttle and brake
    # Acceleration is in the positive direction is expected to be in the range [0 2.0] m/s^2
    throttle = throttle / 2.0 # Convert to percentage
    # Brake is in the negative direction is expected to be in the range [0 -3.5] m/s^2
    brake = brake / 3.5 # Convert to percentage

    can_sends = []
    can_sends.append(self.ava_can.create_auto_command(throttle, brake, steer))

    new_actuators = actuators.as_builder()
    new_actuators.gas = throttle
    new_actuators.brake = brake
    new_actuators.steerOutputCan = steer

    return new_actuators, can_sends



