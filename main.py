from libs.effects import rainbow_cycle
import machine
import neopixel

# CONST
n_leds_total=32
N_LEDS_HEAD_POSITION=31
N_LEDS_WING_SX_START=0
N_LEDS_WING_SX_END=15
N_LEDS_WING_DX_START=16
N_LEDS_WING_DX_END=30
# config
n = 40
p = 5
# set np
np = neopixel.NeoPixel(machine.Pin(p), n)

PIN=5 #d1


