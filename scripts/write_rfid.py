import binascii
from pprint import pprint
import board
import busio
from digitalio import DigitalInOut
from pprint import pprint
from time import sleep

# I2C connection:
from adafruit_pn532.i2c import PN532_I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Manual harware reset
reset_pin = DigitalInOut(board.D6)

# H_Request
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532
pn532.SAM_configuration()

#data = "track:6rqhFgbbKwnb9MLmUQDhG6"

data = input("Enter Spotify URI minus 'spotify:' ")

data = data.encode()

print(data)

byteArray = bytearray(data)
print(byteArray)
print(byteArray[0])

package = []

for i in range(0, len(byteArray), 4):
  chunk = []
  chunk = byteArray[i:i+4]
  
  package.append(chunk)

if len(package) > 20:
      raise Exception("package too large")

pprint(package)

print("Waiting for RFID/NFC card...")
while True:    
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)

    # Try again if no card is available.
    if uid is None:
        continue
    print("Found card with UID:", [hex(i) for i in uid])
    
    # Start at first open block, write all blocks until
    # end of the package
    for i in range(4, len(package) + 4):
      print(i)
      failCount = 0
      
      print(f"block: {i} payload: {package[i-4]}")

      # Check if block was successfully written
      written = pn532.ntag2xx_write_block(i, package[i-4])
      
      if not written:
        failCount += 1
        
        # A few errors is normal, if too many occur card has
        # lost connection
        if failCount == 30:
            raise Exception("unable to read card")
        
        print(f"unable to write block {i}, fail {failCount}")
        sleep(0.2)

      
    break
