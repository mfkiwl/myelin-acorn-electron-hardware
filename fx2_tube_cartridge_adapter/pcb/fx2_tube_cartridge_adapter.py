#!/usr/bin/python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# --------------------------
# fx2_tube_cartridge_adapter
# --------------------------

# by Phillip Pearson

# Adapter board to make it easy to connect an LCSoft Mini board to either an
# Acorn Electron via a Plus 1 cartridge slot, or a BBC Micro or BBC Master via
# the Tube connector, to run Sigrok and David Banks' decode6502 software.

# TODO figure out if it's easier to put the tube connector on the same side of
# the board as the cartridge interface -- if it makes the wiring easier or
# harder.  it probably looks nicest up top.

# Trivial, possibly pointless addition: This can also double as a very simple
# Tube adapter for the Electron, when logic is fitted to match the Tube
# addresses and generate the /TUBE signal).

# TODO check AP6 thread on stardot to see if external tube devices require a
# buffered clock.  If so, there's no point doing this simple option.

# nTUBE <= '0' when nINFC = '0' and A(7 downto 4) = x"E" else '1'

# i.e. nTUBE = !(!nINFC and A7 and A6 and A5 and !A4)
#            = (((nINFC nand 1) and (A4 nand 1)) and (A7 and A6)) nand (A5)

# A 74HCT00 for the nands and a 74HCT08 for the ands should do this nicely.

# nand0 = nINFC nand 1 (= !nINFC)
# nand1 = A4 nand 1 (= !A4)
# and0 = nand0 and nand1 (= !nINFC and !A4)
# and1 = A7 and A6
# and2 = and0 and and1 (= !nINFC and A7 and A6 and !A4)
# nTUBE = nand2 = and2 nand A5 (= !(!nINFC and A7 and A6 and A5 and !A4))
# TODO 74hct00 + capacitor
# TODO 74hct08 + capacitor
# TODO 330R/1k output resistor on nTUBE to limit current if plugged into both
# Electron and BBC for some reason.

import sys, os
here = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.join(here, "../../third_party/myelin-kicad.pretty"))
import myelin_kicad_pcb
Pin = myelin_kicad_pcb.Pin


# Cartridge connector
cart_front = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:acorn_electron_cartridge_edge_connector",
    identifier="CART",
    value="edge connector",
    pins=[
        # front of cartridge / bottom layer of PCB
        Pin( "B1", "5V",    "5V"),
        Pin( "B2", "A10"),
        Pin( "B3", "D3",    "cpu_D3"),
        Pin( "B4", "A11"),
        Pin( "B5", "A9"),
        Pin( "B6", "D7",    "cpu_D7"),
        Pin( "B7", "D6",    "cpu_D6"),
        Pin( "B8", "D5",    "cpu_D5"),
        Pin( "B9", "D4",    "cpu_D4"),
        Pin("B10", "nOE2"),
        Pin("B11", "BA7"),
        Pin("B12", "BA6",   "cpu_A6"),
        Pin("B13", "BA5",   "cpu_A5"),
        Pin("B14", "BA4",   "cpu_A4"),
        Pin("B15", "BA3",   "cpu_A3"),
        Pin("B16", "BA2",   "cpu_A2"),
        Pin("B17", "BA1",   "cpu_A1"),
        Pin("B18", "BA0",   "cpu_A0"),
        Pin("B19", "D0",    "cpu_D0"),
        Pin("B20", "D2",    "cpu_D2"),
        Pin("B21", "D1",    "cpu_D1"),
        Pin("B22", "GND",   "GND"),
        # rear of cartridge / top layer of PCB
        Pin( "A1", "5V",    "5V"),
        Pin( "A2", "nOE"),
        Pin( "A3", "nRST",  "cpu_nRST"),
        Pin( "A4", "RnW",   "cpu_RnW"),
        Pin( "A5", "A8"),
        Pin( "A6", "A13"),
        Pin( "A7", "A12"),
        Pin( "A8", "PHI0",  "cpu_CLK"),
        Pin( "A9", "-5V"),
        Pin("A10", "NC"),
        Pin("A11", "READY", "cpu_READY"),
        Pin("A12", "nNMI",  "cpu_nNMI"),
        Pin("A13", "nIRQ",  "cpu_nIRQ"),
        Pin("A14", "nINFC", "elk_nINFC"),
        Pin("A15", "nINFD"),
        Pin("A16", "ROMQA"),
        Pin("A17", "16MHZ", "elk_16MHz"),
        Pin("A18", "nROMSTB"),
        Pin("A19", "ADOUT"),
        Pin("A20", "ADGND"),
        Pin("A21", "ADIN"),
        Pin("A22", "GND",   "GND"),
    ],
)

tube = myelin_kicad_pcb.Component(
    footprint="Pin_Headers:Pin_Header_Straight_2x20_Pitch2.54mm",
    identifier="TUBE",
    value="tube",
    pins=[
        Pin( 1, "0V", "GND"),
        Pin( 2, "RnW", "cpu_RnW"),
        Pin( 3, "0V", "GND"),
        Pin( 4, "2MHzE", "cpu_CLK"),
        Pin( 5, "0V", "GND"),
        Pin( 6, "/IRQ", "cpu_nIRQ"),
        Pin( 7, "0V", "GND"),
        Pin( 8, "/TUBE", "tube_nTUBE"),
        Pin( 9, "0V", "GND"),
        Pin(10, "/RST", "cpu_nRST"),
        Pin(11, "0V", "GND"),
        Pin(12, "D0", "cpu_D0"),
        Pin(13, "0V", "GND"),
        Pin(14, "D1", "cpu_D1"),
        Pin(15, "0V", "GND"),
        Pin(16, "D2", "cpu_D2"),
        Pin(17, "0V", "GND"),
        Pin(18, "D3", "cpu_D3"),
        Pin(19, "0V", "GND"),
        Pin(20, "D4", "cpu_D4"),
        Pin(21, "0V", "GND"),
        Pin(22, "D5", "cpu_D5"),
        Pin(23, "0V", "GND"),
        Pin(24, "D6", "cpu_D6"),
        Pin(25, "0V", "GND"),
        Pin(26, "D7", "cpu_D7"),
        Pin(27, "0V", "GND"),
        Pin(28, "A0", "cpu_A0"),
        Pin(29, "0V", "GND"),
        Pin(30, "A1", "cpu_A1"),
        Pin(31, "+5V", "5V"),
        Pin(32, "A2", "cpu_A2"),
        Pin(33, "+5V", "5V"),
        Pin(34, "A3", "cpu_A3"),
        Pin(35, "+5V", "5V"),
        Pin(36, "A4", "cpu_A4"),
        Pin(37, "+5V", "5V"),
        Pin(38, "A5", "cpu_A5"),
        Pin(39, "+5V", "5V"),
        Pin(40, "A6", "cpu_A6"),
    ],
)

# TODO lcsoft mini footprint.  need to flip it to look like this, so the lcsoft
# mini board can plug in to the top of the cartridge.

#   R2 R1       L2 L1
#   R4 R3       L4 L3
#    ...         ...
#  R20 R19     L20 L19

# TODO double check against real lcsoft PCB

analyzer = myelin_kicad_pcb.Component(
    footprint="myelin-kicad:lcsoft_mini_flipped",
    identifier="CONN",
    value="lcsoft mini",
    pins=[
        # left side, top to bottom, left to right, with board face up
        # and USB socket upward
        Pin( "L1", "PD5", "cpu_nNMI"),  # TODO add header for BBC test clip
        Pin( "L2", "PD6", "cpu_nRST"),
        Pin( "L3", "PD7", "cpu_A0"),
        Pin( "L4", "GND", "GND"),
        Pin( "L5", "CLK"),
        Pin( "L6", "GND", "GND"),
        Pin( "L7", "RDY0"),
        Pin( "L8", "RDY1"),
        Pin( "L9", "GND", "GND"),
        Pin("L10", "GND", "GND"),
        Pin("L11", "GND", "GND"),
        Pin("L12", "FCLK"),
        Pin("L13", "SCL"),
        Pin("L14", "SDA"),
        Pin("L15", "PB0", "cpu_D0"),
        Pin("L16", "PB1", "cpu_D1"),
        Pin("L17", "PB2", "cpu_D2"),
        Pin("L18", "PB3", "cpu_D3"),
        Pin("L19", "3V3", "3V3"),  # generated from USB
        Pin("L20", "3V3", "3V3"),  # generated from USB

        # right side, top to bottom, left to right
        Pin( "R1", "PD4", "cpu_nIRQ"),
        Pin( "R2", "PD3", "cpu_CLK"),
        Pin( "R3", "PD2", "cpu_READY"),  # TODO add header for BBC test clip
        Pin( "R4", "PD1", "cpu_SYNC"),  # TODO add header for test clip
        Pin( "R5", "PD0", "cpu_RnW"),  # TODO add header to switch Elk/Master
        Pin( "R6", "PA7"),
        Pin( "R7", "PA6"),
        Pin( "R8", "PA5"),
        Pin( "R9", "PA4"),
        Pin("R10", "PA3"),
        Pin("R11", "PA2"),
        Pin("R12", "PA1"),
        Pin("R13", "PA0"),
        Pin("R14", "CTL2"),
        Pin("R15", "CTL1"),
        Pin("R16", "CTL0"),
        Pin("R17", "PB7", "cpu_D7"),
        Pin("R18", "PB6", "cpu_D6"),
        Pin("R19", "PB5", "cpu_D5"),
        Pin("R20", "PB4", "cpu_D4"),
    ],
)

myelin_kicad_pcb.dump_netlist("fx2_tube_cartridge_adapter.net")
