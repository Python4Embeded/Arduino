import time
import json

#常量定义
#SPI
LSBFIRST = 0
MSBFIRST = 1
SPI_CLOCK_DIV4   = 0x00
SPI_CLOCK_DIV16  = 0x01
SPI_CLOCK_DIV64  = 0x02
SPI_CLOCK_DIV128 = 0x03
SPI_CLOCK_DIV2   = 0x04
SPI_CLOCK_DIV8   = 0x05
SPI_CLOCK_DIV32  = 0x06
SPI_MODE0 = 0x00
SPI_MODE1 = 0x04
SPI_MODE2 = 0x08
SPI_MODE3 = 0x0C

class SPI():
    def __init__(self, comm):
        self.comm = comm
        self.ss = 40            #spi pin for select chip
        self.order = MSBFIRST
        self.divider = SPI_CLOCK_DIV4
        self.mode = SPI_MODE0
        self.status = 0
        self.data = {}

    def setSSpin(self, pin_no):
        self.ss = pin_no
    
    def setBitOrder(self, order):
        self.order = order
    
    def setClockDivider(self, divider):
        self.divider = divider
    
    def setDataMode(self, mode):
        self.mode = mode
    
    def begin(self):
        self.status = 1
    
    def end(self):
        self.status = 0

    def write(self, buf):
        self.data["module"] = "spi"
        self.data["status"] = self.status
        self.data["ss"] = self.ss
        self.data["order"] = self.order
        self.data["divider"] = self.divider
        self.data["mode"] = self.mode
        self.data["buf"] = buf

        self.sendMsg()

        return True

    def read(self):
        msg = '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        msg = self.comm.recv_msg()
        self.data = json.loads(msg)    

        return self.data["recv_spi"]

    def sendMsg(self):
        msg = json.dumps(self.data)
        msg += '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        
        return True
