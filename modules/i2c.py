import time
import json

class I2C():
    def __init__(self, comm, No):
        self.comm = comm
        self.No = No                #I2C0 or I2C1
        self.type = "master"        #"master" or "slave"
        self.addr = 0x0A            #slave时的i2c设备地址
        self.data = {}

    def set_type(self, type):
        self.type = type
    
    def set_slave_addr(self, address):
        self.addr = address
    
    def write(self, dev_addr, buf):
        self.data["module"] = "i2c"
        self.data["No"] = self.No
        self.data["type"] = self.type
        self.data["targetAddr"] = dev_addr
        self.data["buf"] = buf

        self.sendMsg()

        return True

    def read(self):
        msg = '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        msg = self.comm.recv_msg()
        self.data = json.loads(msg)    

        return self.data["recv_i2c"]


    def sendMsg(self):
        msg = json.dumps(self.data)
        msg += '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        
        return True
