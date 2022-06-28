from wireless.bt import BluetoothConnection
        
class COMM():
    '''
    初始化通讯接口，可以在:蓝牙、WIFI、串口三个类型中选择。
    输入：
        type: 通讯类型，"bluetooth", "wifi", "serial" 三选一
    '''
    def __init__(self, type):
        self.Type = type
        self.comm = 0

    def comm_open(self, target_name, target_addr):
        if self.Type == "bluetooth":
            '''
            建立蓝牙连接。python接口编程第一步，必须调用。通过蓝牙建立PC与Arduino UNO板的连接。
            '''
            bluetooth_comm = BluetoothConnection(target_name, target_addr)
            if bluetooth_comm.connect_target_device():
                bluetooth_comm.open_sock()    
                self.comm = bluetooth_comm
        if self.Type == "wifi":
            self.comm = 1
        if self.Type == "serial":
            self.comm = 1
        return self.comm

    def comm_close(self):
        
        if self.Type == "bluetooth":
            '''
            关闭蓝牙连接。python接口编程最后一步，结束推出前调用。
            '''
            self.comm.close_sock()
        if self.Type == "wifi":
            self.comm = 0
        if self.Type == "serial":
            self.comm = 0
