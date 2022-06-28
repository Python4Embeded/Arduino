'''
基于bluetooth蓝牙库，封装的蓝牙连接支撑库。
'''
import datetime
import time 
# win10 安装蓝牙依赖包 https://blog.csdn.net/weixin_38676276/article/details/113027104
import bluetooth
 
class BluetoothConnection:
    def __init__(self, target_name, target_addr):
        # 是否找到到设备
        self.find = False
        # 附近蓝牙设备
        self.nearby_devices = None

        self.sock = None
        self.target_name = target_name
        self.target_address = target_addr
 
    def find_nearby_devices(self):
        print("Detecting nearby Bluetooth devices...")
        # 可传参数 duration--持续时间 lookup-name=true 显示设备名
        # 大概查询10s左右
        # 循环查找次数
        loop_num = 3
        i = 0
        try:
            self.nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=5)
            while self.nearby_devices.__len__() == 0 and i < loop_num:
                self.nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=5)
                if self.nearby_devices.__len__() > 0:
                    break
                i = i + 1
                time.sleep(2)
                print("No Bluetooth device around here! trying again {}...".format(str(i)))
            if not self.nearby_devices:
                print("There's no Bluetooth device around here. Program stop!")
            else:
                print("{} nearby Bluetooth device(s) has(have) been found:".format(self.nearby_devices.__len__()), self.nearby_devices)  # 附近所有可连的蓝牙设备s
        except Exception as e:
            # print(traceback.format_exc())
            # 不知是不是Windows的原因，当附近没有蓝牙设备时，bluetooth.discover_devices会报错。
            print("There's no Bluetooth device around here. Program stop(2)!")
 
    def find_target_device(self):
        self.find_nearby_devices()
        if self.nearby_devices:
            for addr, name in self.nearby_devices:
                if self.target_name == name and self.target_address == addr:
                    print("Found target bluetooth device with address:{} name:{}".format(self.target_address, self.target_name))
                    self.find = True
                    break
            if not self.find:
                print("could not find target bluetooth device nearby. "
                      "Please turn on the Bluetooth of the target device.")
 
    def connect_target_device(self):
        res = False
        self.find_target_device()
        
        if self.find:
            print("Ready to connect...")
            res = True
        return res
        
    def open_sock(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.target_address, 1))
        print("Connection successful.")

    def send_msg(self, msg):
        try:
            self.sock.send(msg)
        except Exception as e:
            print("sending message failed.\n", e)
        
    def recv_msg(self):
        data_dtr = ""
        try:
            data = self.sock.recv(1024)
            data_dtr += data.decode()
            if '\n' in data.decode():
                # data_dtr[:-2] 截断"\t\n",只输出数据
                #print(datetime.datetime.now().strftime("%H:%M:%S")+"->"+data_dtr[:-2])
                data_dtr = data_dtr[:-2]
        except Exception as e:
            print("recv message failed.\n", e)
        return data_dtr


    def close_sock(self):
        self.sock.close()
        print("Connection closed.\n")
 
if __name__ == '__main__':
    target_name = "BluetoothV3"
    target_address = "98:D3:32:10:1B:0C"
    BluetoothConnection(target_name, target_address).connect_target_device()
    