import time
import json

class Servo():
    def __init__(self, comm):
        self.comm = comm
        self.pin_no = 0
        self.number = 0
        self.pos = 0
        self.data = {}

    def attach(self, pin_no):
        self.pin_no = pin_no
        self.number = 1
        self.pos = 0
        self.data["module"] = "servo"
        self.data["number"] = self.number
        self.data["pin_no"] = self.pin_no
        self.data["pos"] = self.pos

        self.sendMsg()

        return True

    def detach(self):
        self.number = 0
        self.data["module"] = "servo"
        self.data["number"] = self.number
        self.data["pin_no"] = self.pin_no
        self.data["pos"] = self.pos

        self.sendMsg()

        self.pin_no = 0
        self.pos = 0
        self.data.clear()
        return True

    def write(self, pos):
        self.pos = pos
        data = {}
        data["module"] = "servo"
        data["number"] = self.number
        data["pin_no"] = self.pin_no
        data["pos"] = self.pos

        self.sendMsg()

        return True

    def sendMsg(self):
        msg = json.dumps(self.data)
        msg += '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        return True