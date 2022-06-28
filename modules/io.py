import time
import json

class IO():
    def __init__(self, comm):
        self.data = {}
        self.comm = comm    #comm: 连接句柄
    
    def write(self, digital_value, analog_value):
        '''
        端口写命令
        输入：
            digital_value： 数字端口对应值的列表
            analog_value：模拟端口对应值的列表
            
        '''
        self.data["module"] = "io"
        self.data["digital"] = digital_value
        self.data["analog"] = analog_value

        self.sendMsg()

        return

    def read(self):
        '''
        端口读命令
        返回：
            读取的端口列表值，数字端口值列表、模拟端口值列表
        '''
        msg = '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        msg = self.comm.recv_msg()
        self.data = json.loads(msg)
        analog_value = [x * 5.0 / 1024.0 for x in self.data["analog"]]

        return self.data["digital"], analog_value

    def sendMsg(self):
        msg = json.dumps(self.data)
        msg += '*'
        self.comm.send_msg(msg)
        time.sleep(0.5)
        return True
