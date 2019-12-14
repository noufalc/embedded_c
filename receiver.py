import serial
ser = serial.Serial('/dev/ttyO2', baudrate=1000000)
while True:
    x = ser.readline()
    print x.strip()
ser.close()
