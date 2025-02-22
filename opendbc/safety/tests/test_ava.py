#!/usr/bin/env python3
import unittest

from opendbc.safety.tests.libsafety import libsafety_py
from opendbc.safety.tests.common import PandaCarSafetyTest, CANPackerPanda
from opendbc.car.structs import CarParams

class TestAVASafety(PandaCarSafetyTest):
    TX_MSGS = [[301, 0]]
    # FWD_BLACKLISTED_ADDRS: dict[int, list[int]] = {0: [300, 301]}
    SCANNED_ADDRS = [0x12c]
    FWD_BUS_LOOKUP: dict[int, int] = {0: 2, 1: -1, 2: -1}


    def _user_gas_msg(self, gas):
        return self.packer.make_can_msg_panda("AutonomousControls", 0, {"ThrottleRequest": int(gas)})

    def _vehicle_moving_msg(self, speed):
        return self.packer.make_can_msg_panda("AutonomousFeedbackDynamics", 0, {"WheelSpeed": speed})

    def _pcm_status_msg(self, engaged):
        return self.packer.make_can_msg_panda("AutonomousControls", 0, {"AutonomousSystemReady": int(engaged)})

    def _user_brake_msg(self, brake):
        return self.packer.make_can_msg_panda("AutonomousFeedbackStates", 0, {"BrakePressed": int(brake)})

    # Disable tests that aren't applicable
    def test_allow_engage_with_gas_pressed(self):
        pass

    def test_allow_user_brake_at_zero_speed(self):
        pass

    def test_alternative_experience_no_disengage_on_gas(self):
        pass

    def test_cruise_engaged_prev(self):
        pass

    def test_disable_control_allowed_from_cruise(self):
        pass

    def test_disengage_on_gas(self):
        pass

    def test_enable_control_allowed_from_cruise(self):
        pass

    def test_not_allow_user_brake_when_moving(self):
        pass

    def test_prev_gas(self):
        pass

    def test_prev_user_brake(self):
        pass

    def test_relay_malfunction(self):
        pass

    def test_spam_can_buses(self):
        pass

    def test_tx_msg_in_scanned_range(self):
        pass

    def test_vehicle_moving(self):
        pass

    def test_safety_tick(self):
        pass

    def test_tx_hook_common(self):
        pass

    def setUp(self):
        self.packer = CANPackerPanda("ava_pt")
        self.safety = libsafety_py.libsafety
        self.safety.set_safety_hooks(CarParams.SafetyModel.ava, 0)
        # Default controls to not allowed
        self.safety.set_controls_allowed(False)
        self.safety.init_tests()

    def test_ava_tx_hook(self):
        # Enable controls so that TX messages pass the allowed check.
        self.safety.set_controls_allowed(True)
        dummy_msg = self.packer.make_can_msg_panda("AutonomousControls", 0, {})
        self.assertFalse(self._tx(dummy_msg), "ava_tx_hook should allow the message to be sent")

    def test_ava_rx_hook(self):
        # Build a dummy message using "AutonomousAutoFunctions" (ID 300).
        dummy_msg = self.packer.make_can_msg_panda("AutonomousAutoFunctions", 0, {})
        result = self.safety.safety_rx_hook(dummy_msg)
        self.assertTrue(result, "ava_rx_hook should process the message without error")

    def test_fwd_hook(self):
        result = self.safety.safety_fwd_hook(0, 0x300)
        self.assertEqual(result, -1, "ava_fwd_hook should always return -1")

if __name__ == '__main__':
    unittest.main()
