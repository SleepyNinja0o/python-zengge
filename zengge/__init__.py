# Python module for control of Zengge bluetooth LED bulbs
#
# Copyright 2016 Matthew Garrett <mjg59@srcf.ucam.org>
# Modified by SleepyNinja0o <vb6email@gmail.com>
# It is being ported from the bluepy library to bleak
#
# This code is released under the terms of the MIT license. See the LICENSE
# file for more details.

import time

#from bluepy import btle    #from bluepy lib
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

'''class Delegate(btle.DefaultDelegate):   #Bleak doesn't require a Delegate function
    def __init__(self, bulb):
      self.bulb = bulb
      btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
      if data[5] > 2:
        power = True
      else:
        power = False
      self.bulb.set_state(data[9], data[6], data[7], data[8], power)'''

class zengge:
  def __init__(self, mac):
    self.mac = mac
    self.client = None
    self.device = None
    self.notifyhandle = ""  #handle NOTIFY
    self.statehandle = ""   #handle ffe4
    self.redhandle = ""     #handle ffe6
    self.greenhandle = ""   #handle ffe7
    self.bluehandle = ""    #handle ffe8
    self.rgbwhandle = ""    #handle ffe9
    self.whitehandle = ""   #handle ffea

  def handleNotification(self, cHandle, data):
    if data[5] > 2:
      power = True
    else:
      power = False
    self.set_state(data[9], data[6], data[7], data[8], power)

  def set_state(self, white, red, green, blue, power):
    self.white = white
    self.red = red
    self.green = green
    self.blue = blue
    self.power = power

  async def connect(self):
    #self.device = btle.Peripheral(self.mac, addrType=btle.ADDR_TYPE_PUBLIC)    #from bluepy lib
    #self.device.setDelegate(Delegate(self))    #from bluepy lib

    self.device = await BleakScanner.find_device_by_address(self.mac, timeout=10.0)
    if not self.device:
        raise BleakError(f"A device with address {self.mac} could not be found.")
    self.client = BleakClient(self.device)
    await self.client.connect()
    await self.client.start_notify(self.notifyhandle, self.handleNotification)

    self.get_state()

  async def send_packet(self, uuid, data):
    initial = time.time()
    while True:
      if time.time() - initial >= 10:
        return False
      try:
        #return handle.write(bytes(data), withResponse=True)    #from bluepy lib
        return await self.client.write_gatt_char(uuid, data, response=True)
      except:
        await self.connect()

  async def off(self):
    self.power = False
    packet = bytearray([0xcc, 0x24, 0x33])
    await self.send_packet(self.rgbwhandle, packet)

  async def on(self):
    self.power = True
    packet = bytearray([0xcc, 0x23, 0x33])
    await self.send_packet(self.rgbwhandle, packet)

  async def set_rgb(self, red, green, blue):
    self.red = red
    self.green = green
    self.blue = blue
    self.white = 0
    packet = bytearray([0x56, red, green, blue, 0x00, 0xf0, 0xaa])
    await self.send_packet(self.rgbwhandle, packet)

  async def set_white(self, white):
    self.red = 0
    self.green = 0
    self.blue = 0
    self.white = white
    packet = bytearray([0x56, 0x00, 0x00, 0x00, white, 0x0f, 0xaa])
    await self.send_packet(self.rgbwhandle, packet)

  async def set_rgbw(self, red, green, blue, white):
    self.red = red
    self.green = green
    self.blue = blue
    self.white = white
    await self.send_packet(self.redhandle, bytearray([red]))
    await self.send_packet(self.greenhandle, bytearray([green]))
    await self.send_packet(self.bluehandle, bytearray([blue]))
    await self.send_packet(self.whitehandle, bytearray([white]))

  async def get_state(self):
    await self.send_packet(self.rgbwhandle, bytearray([0xef, 0x01, 0x77]))
    #self.client.waitForNotifications(1.0)    #from bluepy lib

  def get_on(self):
    return self.power

  def get_colour(self):
    return (self.red, self.green, self.blue)

  def get_white(self):
    return self.white
