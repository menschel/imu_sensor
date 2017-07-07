# fxas219002.py
# (C) 2017 Patrick Menschel

import smbus
import struct
import time

FXAS21002_I2C_ID = 0x21
FXAS21002_DEVICE_ID_REG = 0xC
FXAS21002_DEVICEID = 0xD7


FXAS21002_CTRL_REG0 = 0xD


FXAS21002_CTRL_REG1 = 0x13

#control register 1 defines
FXAS21002_CTRL_REG1_RST = (1 << 6) #software reset
FXAS21002_CTRL_REG1_ST = (1 << 5) #selftest
#FXAS21002_CTRL_REG1_DR = (1 << 4) #offset to 3bits to select update frequency
FXAS21002_CTRL_REG1_ACTIVE = (1 << 1) #operation mode selection
FXAS21002_CTRL_REG1_READY = (1 << 0) #operation mode selection


FXAS21002_CTRL_REG2 = 0x14
#control register 2 handles interrupts pins and so on, ignore for now!
FXAS21002_CTRL_INT_CFG_FIFO = (1 << 7)#fifo interrupt pin routing
FXAS21002_CTRL_INT_EN_FIFO = (1 << 6)#fifo interrupt enable
FXAS21002_CTRL_INT_CFG_RT = (1 << 5) #refresh rate interrupt pin routing
FXAS21002_CTRL_INT_EN_RT = (1 << 4)#rate threshold interrupt pin routing
FXAS21002_CTRL_INT_CFG_DRDY = (1 << 3)#data ready interrupt pin routing
FXAS21002_CTRL_INT_EN_DRDY = (1 << 2)#data ready inerrupt enable
FXAS21002_CTRL_IPOL = (1 << 1)#interrupt logic polarity
FXAS21002_CTRL_PP_OD = (1 << 0)#interrupt pin output driver configuration



FXAS21002_CTRL_REG3 = 0x15
#control register 3 handles auto increment of reg pointer for burst reads
#external power control, e.g. set operating mode by pulling INT2 pin low
#range extention of measurements, e.g. higher values, less accuracy
#ignore it for now except for the auto increment
FXAS21002_CTRL_WRAPTOONE = (1 << 3)
FXAS21002_CTRL_EXTCTRLEN = (1 << 2)
FXAS21002_CTRL_FS_DOUBLE = (1 << 0)


class FXAS21002():

    def __init__(self,bus=1,addr=FXAS21002_I2C_ID):
        self.bus = smbus.SMBus(bus)
        self.addr = addr
        self.status = 0
        self.gyro_xyz = []
        #TODO make a worker thread or rather a Timer to get measurements in a specific frequency

    def _write(self,reg,val,size=1):
        if size == 1:
            ret = self.bus.write_byte_data(self.addr,reg,val)
        else:
            raise NotImplementedError()
        return ret

    def _read(self,reg,size=1):
        if size == 1:
            data = self.bus.read_byte_data(self.addr,reg)
        else:
            data = bytearray(self.bus.read_i2c_block_data(self.addr, reg, size))
        return data

    def probe(self):
        dev_id = self._read(FXAS21002_DEVICE_ID_REG)
        if dev_id != FXAS21002_DEVICEID:
            raise RuntimeError("Device not found")
        return

    def configure(self):
        #TODO Handle configuration here later
        #set to standy for configuration
        self._write(FXAS21002_CTRL_REG1,0)

        ctrl_reg0 = 0
        self._write(FXAS21002_CTRL_REG0,ctrl_reg0)
        #range bits are 0b00, so +/-2000degree/s and the value range is +/-32768, factor to multiply is 0,061035156

        #set control bit for register increment wrap to 1st value, as we don't care about satus
        ctrl_reg3 = FXAS21002_CTRL_WRAPTOONE
        self._write(FXAS21002_CTRL_REG3,ctrl_reg3)

        
        #active and ready at least, ready is ignored when active is set
        ctrl_reg1 = (FXAS21002_CTRL_REG1_ACTIVE | FXAS21002_CTRL_REG1_READY)
        self._write(FXAS21002_CTRL_REG1,ctrl_reg1)
        return

    def startup(self):
        try:
            self.probe()
        except RuntimeError:
            print("Device Not Found")
        else:
            self.configure()
        return

    def get_values(self):
        #get 7 bytes from address 0 including
        #  1 byte for status
        #  3x2 bytes for gyro values in xyz direction
        regs = self._read(0,7)
        if len(regs) != 7:
            raise RuntimeError("Not enough bytes to extract values from")
        self.status = regs[0]
        self.gyro_xyz = [(x*0.061035156) for x in struct.unpack(">hhh",regs[1:])]#TODO include the factor for range as it is static to 2000deg/s for now
        return self.status,self.gyro_xyz


if __name__ == "__main__":
    #test code for gyrometer fxas219002
    import time
    FXAS21002_obj = FXAS21002()
    FXAS21002_obj.startup()
    cnt = 0
    try:
        while cnt < 1000:
            #loop for 100 seconds just to get a feel about moving the sensor by hand
            status,gyro_xyz = FXAS21002_obj.get_values()
            print("gyro (deg/s) {0:.2f} {1:.2f} {2:.2f}".format(*gyro_xyz))
            time.sleep(0.1)
            cnt += 1

    except KeyboardInterrupt:
        print("exit")

