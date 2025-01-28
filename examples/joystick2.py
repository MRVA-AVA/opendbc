#!/usr/bin/env python3
from inputs import get_gamepad
import numpy as np
import time

from opendbc.car.structs import CarControl
from opendbc.car.panda_runner import PandaRunner

import threading

class Joystick:
  def __init__(self):
    self.throttle_axis = 'ABS_RZ' # Right Trigger
    self.brake_axis = 'ABS_Z' # Left Trigger
    self.steer_axis = 'ABS_X' # Left Stick X

    # y = mx + b
    self.throttle_params = [0.5, 0.5]
    self.brake_params = [0.5, 0.5]
    self.steer_params = [1.0, 0.0]
    self.min_axis_value = {self.throttle_axis: 0., self.brake_axis: 0., self.steer_axis: 0.}
    self.max_axis_value = {self.throttle_axis: 255., self.brake_axis: 255., self.steer_axis: 255.}
    self.axes_values = {self.throttle_axis: 0., self.brake_axis: 0., self.steer_axis: 0.}

    self.state = {'accel': 0, 'steer': 0}

  def update(self):
    for joystick_event in get_gamepad():
      if joystick_event.code == 'SYN_REPORT':
        continue

      if joystick_event.code in self.axes_values:
        self.max_axis_value[joystick_event.code] = max(joystick_event.state, self.max_axis_value[joystick_event.code])
        self.min_axis_value[joystick_event.code] = min(joystick_event.state, self.min_axis_value[joystick_event.code])

        norm = float(np.interp(joystick_event.state, [self.min_axis_value[joystick_event.code], self.max_axis_value[joystick_event.code]], [-1., 1.]))

        value = 0
        if joystick_event.code == self.throttle_axis:
          value = self.throttle_params[0] * norm + self.throttle_params[1]
          self.axes_values[joystick_event.code] = value
        elif joystick_event.code == self.brake_axis:
          value = self.brake_params[0] * norm + self.brake_params[1]
          self.axes_values[joystick_event.code] = value
        elif joystick_event.code == self.steer_axis:
          value = self.steer_params[0] * norm + self.steer_params[1]
          self.axes_values[joystick_event.code] = value

        self.state['accel'] = self.axes_values[self.throttle_axis] - self.axes_values[self.brake_axis]
        self.state['steer'] = self.axes_values[self.steer_axis]
        continue

def joystick_thread(joystick):
  while True:
    joystick.update()

def main(joystick):
  threading.Thread(target=joystick_thread, args=(joystick,)).start()

  CC = CarControl(enabled=False)
  with PandaRunner() as p:
    while True:
      CC.actuators.accel = float(np.clip(joystick.state['accel'], -1, 1))
      CC.actuators.steer = float(np.clip(joystick.state['steer'], -1, 1))
      # print(CC)
      # p.read()
      p.write(CC)
      time.sleep(0.01)

if __name__ == '__main__':
  joystick = Joystick()
  main(joystick)