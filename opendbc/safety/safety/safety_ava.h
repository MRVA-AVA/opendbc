#pragma once

#include "safety_declarations.h"

static void ava_rx_hook(const CANPacket_t *to_push) {
  UNUSED(to_push);
}

static bool ava_tx_hook(const CANPacket_t *to_send) {

  bool ret = false;

  int addr = GET_ADDR(to_send);

  if (addr == 0x12C) {
    ret = true;
  } else if (addr == 0x12D){
    ret = true;
  }


  return ret;
}

static int ava_fwd_hook(int bus_num, int addr) {
  UNUSED(bus_num);
  UNUSED(addr);
  int bus_fwd = -1;

  return bus_fwd;
}

static safety_config ava_init(uint16_t param) {
  UNUSED(param);
  return (safety_config){NULL, 0, NULL, 0};
}

const safety_hooks ava_hooks = {
  .init = ava_init,
  .rx = ava_rx_hook,
  .tx = ava_tx_hook,
  .fwd = ava_fwd_hook,
};