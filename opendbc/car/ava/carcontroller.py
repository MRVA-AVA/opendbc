from opendbc.car.interfaces import CarControllerBase
from opendbc.can.packer import CANPacker
from opendbc.car import Bus
from opendbc.car.ava.avacan import AvaCan

class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.pt])
    self.ava_can = AvaCan(self.packer)

  def update(self, CC, CS, now_nanos):
    actuators = CC.actuators
    can_sends = []

    throttle = 0
    brake = 0
    steering = actuators.steeringAngleDeg
    if (actuators.accel > 0.0):
        throttle = 1000*actuators.accel
        brake = 0
    else:
        throttle = 0
        brake = -1500*actuators.accel

    can_sends.append(self.ava_can.create_auto_command(throttle, brake, steering))

    new_actuators = 0

    return new_actuators, can_sends

