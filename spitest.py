from Adafruit_BBIO.SPI import SPI
import Adafruit_BBIO.GPIO as GPIO
import time
#From Adafruit Learning System:
#https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/spi     
#spi = SPI(bus, device) #/dev/spidev<bus>.<device>
#spi = SPI(0,0) #/dev/spidev1.0
#spi = SPI(0,1) #/dev/spidev1.1
#spi = SPI(1,0) #/dev/spidev2.0
#spi = SPI(1,1) #/dev/spidev2.1

flash_handler = SPI(1,0) 

flash1_cs = "P8_43"
flash2_cs = "P8_44"
flash3_cs = "P8_45"

GPIO.setup(flash1_cs, GPIO.OUT)
GPIO.setup(flash2_cs, GPIO.OUT)
GPIO.setup(flash3_cs, GPIO.OUT)
GPIO.output(flash1_cs, GPIO.HIGH)
GPIO.output(flash2_cs, GPIO.HIGH)
GPIO.output(flash3_cs, GPIO.HIGH)


def initFlash(flash_handler, cs):
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2([0xA1, 0xAA])
    GPIO.output(cs, GPIO.HIGH)
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2([0x06])
    GPIO.output(cs, GPIO.HIGH)
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2([0x01, 0x00])
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.001)


def readStatus(flash_handler, cs):
    GPIO.output(cs, GPIO.LOW)
    data = '[{}]'.format(', '.join(hex(x) for x in flash_handler.xfer2([0x05, 0x00])))
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.001)
    return data[7:-1]

def readID(flash_handler, cs):
    GPIO.output(cs, GPIO.LOW)
    data = '[{}]'.format(', '.join(hex(x) for x in flash_handler.xfer2([0x9F, 0x00, 0x00, 0x00])))
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.001)
    #print data[7:-1]
    return data[7:-1]

def waitForReady(flash_handler, cs):
    i = 0
    while True:
        GPIO.output(cs, GPIO.LOW)
        data = flash_handler.xfer2([0x05, 0xFF])
        GPIO.output(cs, GPIO.HIGH)
        time.sleep(0.0001)
        if data[1] & 1 == 0:
            #print data[1]
            break

def totalErase(flash_handler, cs):
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2([0x06])
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.0001)
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2([0x60])
    GPIO.output(cs, GPIO.HIGH)
    waitForReady(flash_handler, cs)
    #print "Erased"

def writeByte(flash_handler, address, data, cs):
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2([0x06])
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.0001)
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2([0x02, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF, data])
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.0001)

def readBytes(flash_handler, address, length, cs):
    time.sleep(0.0001)
    xfer_list = [0x03]
    xfer_list += [(address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
    xfer_list += [0xFF] * length
    GPIO.output(cs, GPIO.LOW)
    out = flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.0001)
    return out[4:]

def erase4kbSector(flash_handler, sectorNo, cs):
    xfer_list = [0x06]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    xfer_list = [0x20]
    address = sectorNo * 4 * 1024 
    xfer_list += [(address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    waitForReady(flash_handler, cs)
    time.sleep(0.0001)


def erase32kbSector(flash_handler, sectorNo, cs):
    xfer_list = [0x06]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    xfer_list = [0x52]
    address = sectorNo * 32 * 1024
    xfer_list += [(address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    waitForReady(flash_handler, cs)
    time.sleep(0.0001)


def erase64kbSector(flash_handler, sectorNo, cs):
    xfer_list = [0x06]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    xfer_list = [0x52]
    address = sectorNo * 64 * 1024
    xfer_list += [(address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    waitForReady(flash_handler, cs)
    time.sleep(0.0001)


def writeBytes(flash_handler, address, data, cs):
    xfer_list = [0x06]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.0001)
    xfer_list = [0xAD]
    xfer_list += [(address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
    x = data[0:2]
    xfer_list += x
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.001)
    waitForReady(flash_handler, cs)
    for i in range(2, len(data), 2):
        xfer_list = [0xAD]
        x = data[i:i+2]
        xfer_list += x
        #xfer_list += [(address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
        GPIO.output(cs, GPIO.LOW)
        flash_handler.xfer2(xfer_list)
        GPIO.output(cs, GPIO.HIGH)
        waitForReady(flash_handler, cs)
    xfer_list = [0x04]
    GPIO.output(cs, GPIO.LOW)
    flash_handler.xfer2(xfer_list)
    GPIO.output(cs, GPIO.HIGH)
    time.sleep(0.0001)

if __name__ == "__main__":
    initFlash(flash_handler, flash1_cs)
    initFlash(flash_handler, flash2_cs)
    initFlash(flash_handler, flash3_cs)
    print readStatus(flash_handler, flash1_cs)
    print readStatus(flash_handler, flash2_cs)
    print readStatus(flash_handler, flash3_cs)
    print readID(flash_handler, flash1_cs)
    print readID(flash_handler, flash2_cs)
    print readID(flash_handler, flash3_cs)
    totalErase(flash_handler, flash1_cs)
    totalErase(flash_handler, flash2_cs)
    totalErase(flash_handler, flash3_cs)
#    #writeByte(flash_handler,0x00,33)
#    #writeByte(flash_handler,0x01,34)
#    erase4kbSector(flash_handler, 0)
#    f.write(datetime.datetime.now())
    data1 = [i for i in range(100)]
    data2 = [2*i for i in range(100)]
    data3 = [3*i for i in range(100)]
    writeBytes(flash_handler, 0x000000, data1, flash1_cs)
    writeBytes(flash_handler, 0x000000, data2, flash2_cs)
    writeBytes(flash_handler, 0x000000, data3, flash3_cs)
    print readBytes(flash_handler, 0x00, 32, flash1_cs)
    print readBytes(flash_handler, 0x00, 32, flash2_cs)
    print readBytes(flash_handler, 0x00, 32, flash3_cs)
    erase4kbSector(flash_handler, 0, flash1_cs)
    erase4kbSector(flash_handler, 0, flash2_cs)
    erase4kbSector(flash_handler, 0, flash3_cs)
    print readBytes(flash_handler, 0x00, 32, flash1_cs)
    print readBytes(flash_handler, 0x00, 32, flash2_cs)
    print readBytes(flash_handler, 0x00, 32, flash3_cs)
#    #print readBytes(flash_handler, 0x00, 200)
#    erase4kbSector(flash_handler, 0)
#    data = [i for i in range(256)]
#    writeBytes(flash_handler, 0x000000, data)
#    print readBytes(flash_handler, 0x00, 1<<8)
#    erase4kbSector(flash_handler, 0)
    flash_handler.close()
