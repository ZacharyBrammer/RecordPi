import time
import board
import digitalio

in1 = digitalio.DigitalInOut(board.D23)
in1.direction = digitalio.Direction.OUTPUT

in2 = digitalio.DigitalInOut(board.D24)
in2.direction = digitalio.Direction.OUTPUT

while True:
	direction = input("Which way motor go: 1 = in1 high, 2 = in2 high\n")
	if int(direction) == 1:
		in1.value = True
		in2.value = False
		print(str(in1.value) + " " + str(in2.value))
	elif int(direction) == 2:
		in1.value = False
		in2.value = True
		print(str(in1.value) + " " + str(in2.value))
	else:
		in1.value = False
		in2.value = False
		print(str(in1.value) + " " + str(in2.value))
