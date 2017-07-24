# fxos8700cq.py
# (C) 2017 Patrick Menschel

import smbus
import struct
import time
import numpy as np

FXOS8700CQ_I2C_ID = 0x1F
FXOS8700CQ_DEVICEID = 0xC7

FXOS8700CQ_DEVICE_ID_REG = 0xD
FXOS8700CQ_XYZ_DATA_CFG = 0x0E
FXOS8700CQ_CTRL_REG1 = 0x2A
FXOS8700CQ_M_CTRL_REG1 = 0x5B
FXOS8700CQ_M_CTRL_REG2 = 0x5C


class FXOS8700CQ():

    def __init__(self,bus=1,addr=FXOS8700CQ_I2C_ID):
        self.bus = smbus.SMBus(bus)
        self.addr = addr
        self.status = 0
        self.acc_values = []
        self.mag_values = []
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
        dev_id = self._read(FXOS8700CQ_DEVICE_ID_REG)
        if dev_id != FXOS8700CQ_DEVICEID:
            raise RuntimeError("Device not found")
        return

    def configure(self):
        #TODO Handle configuration here later
        #set to standy for configuration
        self._write(FXOS8700CQ_CTRL_REG1,0)

        #setup magnetometer registers m_ctrl_reg[1..2]
        m_ctrl_reg1 = 0x1F
        self._write(FXOS8700CQ_M_CTRL_REG1,m_ctrl_reg1)

        m_ctrl_reg2 = 0x20
        self._write(FXOS8700CQ_M_CTRL_REG2,m_ctrl_reg2)

        #setup xyz data configuration register
        xyz_data_cfg = 0x01
        self._write(FXOS8700CQ_XYZ_DATA_CFG,xyz_data_cfg)

        #setup control register 1 and activate the device with bit 0x01
        ctrl_reg1 = 0x0D
        self._write(FXOS8700CQ_CTRL_REG1,ctrl_reg1)
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
        #get 13 bytes from address 0 including
        #  1 byte for status
        #  3x2 bytes for accelerometer values in xyz direction
        #  3x2 bytes for magnetometer values in xyz direction
        regs = self._read(0,13)
        if len(regs) != 13:
            raise RuntimeError("Not enough bytes to extract values from")
        self.status = regs[0]
        self.acc_xyz = [((x>>2)*0.488) for x in struct.unpack(">hhh",regs[1:7])]#TODO include the factor for range as it is static to 4g for now
        self.mag_xyz = [(x*0.1) for x in struct.unpack(">hhh",regs[7:])]
        return self.status,self.acc_xyz,self.mag_xyz


def selftest(testmode="standard deviation"):
    #test code for accelerometer fxos8700cq
    import time
    FXOS8700CQ_obj = FXOS8700CQ()
    FXOS8700CQ_obj.startup()
    testcount = 100
    testcycle = 0.1
    if testmode == "standard deviation":
        print("do not move the sensor while standard deviation is calculated - takes about {0} seconds".format(testcount*testcycle))
        cnt = 0
        vals_accel = []
        vals_mag = []
        try:
            while cnt < testcount:
                #loop for 100 seconds just to get a feel about moving the sensor by hand
                status,accel_xyz,mag_xyz = FXOS8700CQ_obj.get_values()
                #print("accel (mg) {0:.2f} {1:.2f} {2:.2f}".format(*accel_xyz))
                #print("mag (uT) {0:.2f} {1:.2f} {2:.2f}".format(*mag_xyz))
                time.sleep(testcycle)
                cnt += 1
                vals_accel.append(accel_xyz)
                vals_mag.append(mag_xyz)

        except KeyboardInterrupt:
            print("exit")

        #calculate the standard deviation
        std_dev_accel = [np.std(np.array([val[i] for val in vals_accel])) for i in range(2)]
        std_dev_accel.append(np.std(np.array([val[2]-1000 for val in vals_accel])))

        print("Standard Deviation for fxos8700cq accelerometer\nx\t{0}\ny\t{1}\nz\t{2}".format(*std_dev_accel))

        std_dev_mag = [np.std(np.array([val[i] for val in vals_mag])) for i in range(3)]
        
        print("Standard Deviation for fxos8700cq magnetometer\nx\t{0}\ny\t{1}\nz\t{2}".format(*std_dev_mag))
            



        


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--command", dest="command", default='standard deviation',
                      help="COMMAND to execute", metavar="COMMAND")
    (options, args) = parser.parse_args()
    selftest(testmode=options.command)
 
