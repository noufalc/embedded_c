import serial
ser = serial.Serial('/dev/ttyO1')
print(ser.name)
while True:
    val = raw_input()
    ser.write(val + '\n')
ser.close()

