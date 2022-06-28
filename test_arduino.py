from ctypes.wintypes import PINT
import Arduino_UNO as uno
#import Arduino_UNO.Servo as servo
import time

target_name = "BluetoothV3"
target_address = "98:D3:32:10:1B:0C"

HIGH = 1
LOW = 0

if __name__ == '__main__':

    #创建蓝牙连接
    bl_com = uno.Wireless_Setup(target_name, target_address)
    ############
    #不需要设置pinMode函数，系统会自动设置输入输出模式。
    ############
    #数字端口D5输出低电平
    #uno.digitalWrite(5, LOW, bl_com)
    #数字端口D2输出高电平
    uno.digitalWrite(2, HIGH, bl_com)
    
    #读取数字端口D9的数值
    pin  = 2
    a = uno.digitalRead(pin, bl_com)
    print("digital read: ", a)
    time.sleep(0.2)

    #数字端口D3输出PWM，占空比为：50/256
    uno.analogWrite(3, 100, bl_com)

    myservo = uno.Servo(bl_com)
    myservo.attach(10)
    print("mysero attach ok")
    time.sleep(2)
    myservo.write(180)
    print("myservo move")
    #time.sleep(5)
    myservo.detach()
    print("servo bye")

    #读取模拟端口A0的电压值
    #for i in range (100):
    #    b = uno.analogRead(5, bl_com)
    #    print("analog read: ", b)
    #    time.sleep(0.2)

    #关闭蓝牙连接
    uno.Wireless_Close(bl_com)
    