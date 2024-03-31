import board
import busio
from digitalio import DigitalInOut
from pprint import pprint
from time import sleep

from adafruit_pn532.i2c import PN532_I2C

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)

# Manual hardware reset
reset_pin = DigitalInOut(board.D6)

# H_Request
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532
pn532.SAM_configuration()

cardData = []

print("Waiting for RFID/NFC card...")
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    
    print(".", end="")
    # Try again if no card is available.
    if uid is None:
        continue
    print("Found card with UID:", [hex(i) for i in uid])
    
    # Read first 20 data blocks of card
    for i in range(4, 24):
      print(i)
      failCount = 0
    
      while True:
        block = pn532.ntag2xx_read_block(i)
        if block is not None:
          cardData.append([hex(x) for x in block])
          break
        else:
          failCount += 1
          
          # A few errors is normal, if too many occur card has
          # lost connection
          if failCount == 30:
            raise Exception("unable to read card")
          
          print(f"unable to read block {i}, fail {failCount}")
          sleep(0.2)
    break

print(uid)
pprint(cardData)