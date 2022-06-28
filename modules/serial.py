import time
import json

class Serial():
    def __init__(self, comm):
        self.comm = comm
        self.No = 1
        self.snd_buf = " "
        self.recv_buf = " "
        self.baud = 9600
        self.data = {}
        
    def begin(self, baud):
        self.baud = baud
        return True

    def set_SerialNo(self, no):
        self.No = no
        return True
        
    def write(self, str):
        self.snd_buf = str
        self.data["module"] = "serial"
        self.data["No"] = self.No
        self.data["baud"] = self.baud
        self.data["buf"] = self.snd_buf

        self.sendMsg()

        return True

    def read(self):
        msg = '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        msg = self.comm.recv_msg()
        self.data = json.loads(msg)    

        return self.data["recv_serial"]

    def available(self):
        msg = '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        msg = self.comm.recv_msg()
        self.data = json.loads(msg)    

        return self.data["available"]

    def sendMsg(self):
        msg = json.dumps(self.data)
        msg += '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        return True