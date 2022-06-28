'''
基于bluetooth_lib库，建立Arduino UNO板 Python 编程接口库。
'''
import time
import json
from modules.io import IO
from modules.led import LED
from modules.i2c import I2C
from modules.serial import Serial
from modules.spi import SPI
from modules.servo import Servo
from comm.comm import COMM


class ArduinoMEGA2560():
    def __init__(self, target_name, target_addr) -> None:

        self.target_name = target_name          #通讯连接目标电路板的设备名称
        self.target_addr = target_addr          #通讯连接目标电路板的设备地址

        self.comm_bluethooth = COMM("bluetooth")     #缺省使用蓝牙连接
        self.comm = self.comm_bluethooth.comm_open(self.target_name, self.target_addr)

        self.io = IO(self.comm)                 #初始化电路板IO端口
        self.led = LED(self.comm)               #初始化电路板LED
        self.servo = Servo(self.comm)           #初始化电路板Servo电机端口
        self.i2c = I2C(self.comm)               #初始化电路板I2C端口
        self.serial = Serial(self.comm)         #初始化电路板Serial端口
        self.spi = SPI(self.comm)               #初始化电路板SPI端口

        self.data = {}                          #初始化数据结构
        self.data["board"] = "ArduinoMEGA2560"  #设置电路板名称
        
        self.analog = [0] * 6                   #电路板模拟端口初始化
        self.digital = [0] * 14                 #电路板数字端口初始化
        
        self.comm_tx_pin = 7                    #电路板与PC通讯模块所使用的端口定义
        self.comm_rx_pin = 8                    #电路板与PC通讯模块所使用的端口定义

        self.led_pin = 13                       #定义电路板LED所在端口
        
        #通讯模块占用端口设置为1，避免通讯被干扰
        self.digital[self.comm_tx_pin] = self.digital[self.comm_rx_pin] = 1

        #发送电路板标识信息
        self.sendMsg()

        pass

    def digitalWrite(self, pin, val):
        '''
        等同于Arduino编程的digitalWrite语句。
        输入：
            pin： 数字端口，直接用数字表示
            val：端口要输出的值，1表示高，0表示低
            
        '''
        self.digital[pin] = val
        self.io.write(self.digital, self.analog)
        return True

    def digitalRead(self, pin):
        '''
        等同于Arduino编程的digitalRead语句。
        输入：
            pin： 数字端口，直接用数字表示
            
        返回：
            读取的数字端口值：1或者0
        '''
        digital, analog = self.io.read()
        
        return digital[pin]

    def analogRead(self, pin):
        '''
        等同于Arduino编程的analogRead语句。
        输入：
            port： 模拟端口（A0-A5），直接用数字表示对应的端口号。例如：输入0，表示A0
        返回：
            读取的模拟端口电压值：0-5v之间的浮点数。
        '''
        digital, analog = self.io.read()
        
        return analog[pin]

    def analogWrite(self, pin, val):
        '''
        等同于Arduino编程的analogWrite语句，输出PWM信号。
        输入：
            port： 数字端口，直接用数字表示
            val：端口要输出的值：0-255之间，占空比为：val/256。
            bl_com: 蓝牙连接句柄
        '''
        self.digital[pin] = val
        self.io.write(self.digital, self.analog)
        return True

    def i2c_set_type(self, type):
        '''
        设置I2C通讯时，电路板属性：master or slave
        输入：
            type： "master" or "slave"
            
        '''
        self.i2c.set_type(type)
        return True
    
    def i2c_set_slaveAddr(self, addr):
        '''
        设置I2C通讯，当电路板属性为slave时，电路板的从机设备地址
        输入：
            addr：单字节16进制数
            
        '''
        self.i2c.set_slave_addr(addr)
        return True

    def i2c_write(self, dev_addr, buf):
        '''
        设置I2C通讯，电路板发送字符串到目标地址
        输入：
            dev_addr:发送目标设备地址。
            buf: 发送信息    
        '''
        self.i2c.write(dev_addr, buf)
        return True
    
    def i2c_read(self):
        '''
        设置I2C通讯，电路板接收信息
        输入：
            None
        返回：
            接收到的信息
        '''
        recv_buf = self.i2c.read()
        return recv_buf

    def led_on(self):
        '''
        点亮电路板LED
        输入：
            None
        '''
        self.digitalWrite(self.led_pin, 1)
        return True

    def led_off(self):
        '''
        关闭电路板LED
        输入：
            None
        '''
        self.digitalWrite(self.led_pin, 0)
        return True

    def set_led_pin(self, led_pin):
        '''
        设置电路板LED所在端口
        输入：
            led_pin: LED对应端口，缺省为D13
        '''
        self.led_pin = led_pin
        return True

    def servo_attach(self, pin):
        '''
        设置舵机所在端口。由于使用Arduino的Servo库，只支持最多连接两个舵机，端口9和10
        输入：
            pin:舵机连接端口，9或者10，二选一
        '''
        self.servo.attach(pin)
        return True

    def servo_detach(self):
        '''
        解除舵机所连接端口。
        输入：
            None
        '''
        self.servo.detach()
        return True

    def servo_write(self, pos):
        '''
        设置舵机转动到目标角度。
        输入：
            pos: 舵机目标角度
        '''
        self.servo.write(pos)
        return True

    def spi_setSSpin(self, pin):
        '''
        设置SPI通讯设备选择信号的端口。
        输入：
            pin: 端口号
        '''
        self.spi.setSSpin(pin)
        return True

    def spi_setBitOrder(self, order):
        '''
        设置SPI通讯时信号发送的顺序。
        输入：
            order: LSBFIRST or MSBFIRST
        '''
        self.spi.setBitOrder(order)
        return True

    def spi_setClockDivider(self, divider):
        '''
        设置SPI通讯时钟信号分频。
        输入：
            divider: 分频数
        '''
        self.spi.setClockDivider(divider)
        return True

    def spi_setDataMode(self, mode):
        '''
        设置SPI通讯时数据模式。
        输入：
            mode：模式，查spi.py中定义
        '''
        self.spi.setDataMode(mode)
        return True

    def spi_begin(self):
        '''
        设置SPI通讯开始。
        输入：
            None
        '''
        self.spi.begin()
        return True

    def spi_end(self):
        '''
        设置SPI通讯结束。
        输入：
            None
        '''
        self.spi.end()
        return True
    
    def spi_write(self, buf):
        '''
        设置SPI通讯发送信息。
        输入：
            buf: 要发送的字符串
        '''
        self.spi.write(buf)
        return True

    def spi_read(self):
        '''
        设置SPI通讯接收信息。
        输入：
            None
        返回：
            接收到的信息
        '''
        buf = self.spi.read()
        return buf

    def serial_begin(self, baud):
        '''
        设置UART串口Serial通讯。
        输入：
            baud：波特率
        '''
        self.serial.begin(baud)
        return True

    def serial_set_SerialNo(self, no):
        '''
        设置UART串口Serial通讯的串口号。由于板子支持多个串口，设置使用的串口好。
        输入：
            no：串口号
        '''
        self.serial.set_SerialNo(no)
        return True
        
    def serial_write(self, str):
        '''
        设置UART串口Serial发送信息。
        输入：
            str：发送字符串
        '''
        self.serial.write(str)
        return True

    def serial_read(self):
        '''
        设置UART串口Serial读取信息。
        输入：
            None
        返回：
            读取的信息
        '''
        buf = self.serial.read()
        return buf

    def serial_available(self):
        '''
        判断UART串口Serial是否读到信息。
        输入：
            None
        返回：
            1，串口收到信息
            0，串口没有收到信息
        '''
        available = self.serial.available()    
        return available

    def set_comm_pin(self, tx_pin, rx_pin):
        '''
        设置电路板连接通讯模块端口。
        输入：
            tx_pin: 通讯模块tx端口
            rx_pin: 通讯模块rx端口
        '''
        self.comm_tx_pin = tx_pin
        self.comm_rx_pin = rx_pin
        return True

    def sendMsg(self):
        '''
        信息发送：PC -> Arduino
        输入：
            None
        '''
        msg = json.dumps(self.data)
        msg += '*'
        self.comm.send_msg(msg)
        time.sleep(0.2)
        return True

    def clearIO(self):
        '''
        初始化IO端口
        '''
        self.digital = [0] * 14
        self.analog = [0] * 6
        self.digital[self.comm_tx_pin] = self.digital[self.comm_rx_pin] = 1
        return True
    
    def comm_close(self):
        '''
        PC通讯关闭
        '''
        self.comm_bluethooth.comm_close()
        return True

if __name__ == '__main__':
    
    target_name = "BluetoothV3"
    target_address = "98:D3:32:10:1B:0C"
    
    pass    
    