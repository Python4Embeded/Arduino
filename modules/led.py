import time
import json

class LED():
    def __init__(self, comm):
        self.comm = comm
        self.led_pin = 13
        self.data = {}

    def set_led_pin(self, pin):
        self.led_pin = pin
        
    def on(self):  
        self.data["model"] = "led"
        self.data["led_pin"] = self.led_pin
        self.data["led_on"] = 1
        
        self.sendMsg()
        
        return True

    def off(self):        
        self.data["model"] = "led"
        self.data["led_pin"] = self.led_pin
        self.data["led_on"] = 0
        
        self.sendMsg()

        return True

    def sendMsg(self):
        msg = json.dumps(self.data)
        msg += '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        return True
