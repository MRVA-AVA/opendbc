#!/usr/bin/env python3
from inputs import get_gamepad
import numpy as np
import time
import argparse
import curses

from opendbc.car.structs import CarControl
from opendbc.car.panda_runner import PandaRunner

import threading

class Mock:
  def __init__(self):
    self.state = {'accel': 0, 'steer': 0}
    self.running = True

  def update(self):
    time.sleep(100)

class Keyboard:
  def __init__(self):
    self.state = {'accel': 0, 'steer': 0}
    self.running = True  # To manage the thread's lifecycle

  def update(self, stdscr):
    stdscr.nodelay(True)  # Make getch non-blocking
    stdscr.addstr("Press 'w' to accelerate, 's' to brake, 'a' to steer left, 'd' to steer right. Press 'q' to quit.\n")
    while self.running:
      try:
        key = stdscr.getch()
        if key == ord('w'):
          self.state['accel'] = 1
        elif key == ord('s'):
          self.state['accel'] = -1
        elif key == ord('a'):
          self.state['steer'] = -1
        elif key == ord('d'):
          self.state['steer'] = 1
        elif key == ord('q'):
          self.running = False  # Exit the loop on 'q'
        else:
          self.state['accel'] = 0
          self.state['steer'] = 0
        time.sleep(0.05)  # Small delay to reduce CPU usage
      except Exception as e:
          stdscr.addstr(f"Error: {e}\n")
          self.running = False
          break

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
    self.running = True  # To manage the thread's lifecycle

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

def keyboard_thread(keyboard):
  curses.wrapper(keyboard.update)

def joystick_thread(joystick):
  while joystick.running:
    joystick.update()

def mock_thread(mock):
  while mock.running:
    mock.update()

def main(controller):
  try:
    with PandaRunner() as p:
      CC = CarControl(enabled=False)
      while controller.running:
        CC.actuators.accel = float(np.clip(controller.state['accel'], -1, 1))
        CC.actuators.steer = float(100*np.clip(controller.state['steer'], -1, 1))

        # p.read()
        p.write(CC)

        time.sleep(0.01)
  except KeyboardInterrupt:
      controller.running = False
  print("Exiting...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the car interface with a joystick or keyboard.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--mode', choices=['keyboard', 'joystick', 'mock'], default='keyboard')
    args = parser.parse_args()

    if args.mode == 'keyboard':
        controller = Keyboard()
        threading.Thread(target=keyboard_thread, args=(controller,), daemon=True).start()
    elif args.mode == 'joystick':
        controller = Joystick()
        threading.Thread(target=joystick_thread, args=(controller,), daemon=True).start()
    elif args.mode == 'mock':
        controller = Mock()
        threading.Thread(target=mock_thread, args=(controller,), daemon=True).start()

    main(controller)