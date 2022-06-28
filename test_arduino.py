from ctypes.wintypes import PINT
import Arduino_UNO as uno
#import Arduino_UNO.Servo as servo
import time

target_name = "BluetoothV3"
target_address = "98:D3:32:10:1B:0C"

HIGH = 1
LOW = 0

if __name__ == '__main__':

    #初始化arduino uno板
    arduino = uno.ArduinoUNO(target_name, target_address)
    ############
    #数字端口D5输出低电平
    arduino.digitalWrite(5, LOW)
    #数字端口D2输出高电平
    arduino.digitalWrite(2, HIGH)
    
    #读取数字端口D9的数值
    pin  = 2
    a = arduino.digitalRead(pin)
    print("digital read: ", a)
    time.sleep(0.2)

    #数字端口D3输出PWM，占空比为：50/256
    arduino.analogWrite(3, 100)

    arduino.servo_attach(10)
    print("sero attach ok")
    time.sleep(2)
    arduino.servo_write(180)
    print("servo move")
    #time.sleep(5)
    arduino.servo_detach()
    print("servo bye")

    #读取模拟端口A0的电压值
    for i in range (100):
        b = arduino.analogRead(5)
        print("analog read: ", b)
        time.sleep(0.2)

    #关闭蓝牙连接
    arduino.comm_close()
    