# Python for Arduino Board

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/python4embeded/arduinoUNO/">
    <img src="images/python4embeded.png" alt="Logo" width="345" height="80">
  </a>

  <h3 align="center">Python Package for Arduino</h3>
  <p align="center">
    Arudino板的Python包。目前支持UNO和MEGA2560。
    <br />
    <a href="https://github.com/python4embeded/arduinoUNO/docs"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/python4embeded/arduinoUNO">查看Demo</a>
    ·
    <a href="https://github.com/python4embeded/arduinoUNO/issues">报告Bug</a>
    ·
    <a href="https://github.com/python4embeded/arduinoUNO/issues">提出新特性</a>
  </p>

</p>

#### 项目说明：

作为Python for Embeded System项目中的组成部分，本项目实现Arudino板的python编程接口。
<br />

#### 项目特点：<br />

- 用户在PC端编写python程序，通过无线方式（蓝牙或WIFI），发送到Arduino板执行。
- 由于用户程序在PC端运行，可以调用任何python库，充分发挥python的特色。
- 对于控制Arduino硬件端口的语句，和Arduino本身编程环境中C语言的函数名尽量保持一致。
- Arduino板需要连接蓝牙或WIFI模块，程序采用的是普通IO口模拟串口的功能。Arduino板自带的串口，可以作为监测电路板运行用。
- 通过Arduino的舵机库支持使用舵机。

## 目录

- [上手指南](#上手指南)
  - [安装前的配置要求](#安装前的配置要求)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [开发的架构](#开发的架构)
- [贡献者](#贡献者)
  - [如何参与开源项目](#如何参与开源项目)
- [版本控制](#版本控制)
- [作者](#作者)

### 上手指南

  PC与电路板之间的通讯：<br />
  - 无线：蓝牙/WIFI
  - 有线：USB/串口

#### 安装前的配置要求

  对于使用蓝牙模块进行通讯的模式，需要安装python bluetooth库：pybluez

##### Ubuntu

1. 安装所需支持库
```sh
sudo apt-get install libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev
```
2. 安装Python的蓝牙库
```sh
pip  install pybluez
```
3. 测试pybluez是否安装正确：
   运行python，输入：
   ```sh
   import bluetooth
   ```
   如果未报错，表示安装成功。

##### Windows

1. 下载Python蓝牙支持包: [Pybluez for Windows](https://github.com/python4embeded/arduinoUNO/blob/main/PyBluez_Win/PyBluez-0.22-cp35-none-win_amd64.whl)
2. 由于Python的蓝牙支持包最高只能支持到Python 3.5，切记Python版本不能高。建议使用Anaconda进行Python多版本管理。
3. 安装下载的蓝牙支持包
```sh
pip install PyBluez-0.22-cp35-none-win_amd64.whl
```
4. 测试pybluez是否安装正确：
   运行python，输入：
   ```sh
   import bluetooth
   ```
   如果未报错，表示安装成功。

#### **安装步骤**

1. 直接安装
```sh
pip install pyArduino
```
2. 或者 Clone the repo
```sh
git clone https://github.com/Python4Embeded/Arduino.git
```
3. Arduino板端安装：
- Arduino IDE需要安装ArduinoJson支持库：在Arduino IDE中，选择：项目->加载库->管理库。在对话框中选择ArduinoJson，进行安装。
- 安装Arduino目录中不同Arduino型号对应目录的程序，如：ArduinoUNO的程序为：ArduinoUNO.ino程序，直接下载到电路板上。
- 目前支持UNO和MEGA2560
- 可以打开Arduino的串口监测程序，监测电路板运行情况。
- 连接蓝牙模块：目前程序中连接蓝牙的串口是通过D7（RX），D8（TX）进行模拟，需要把蓝牙模块的TxD连接到D7，RxD连接到D8。注意不要接错。接其他端口，请自行修改定义。

4. 运行：test_ArduinoUNO.py进行测试。看文件注释即可了解依赖包的工作方式。

### 文件目录说明

```
filetree 
├── /images/
├── /PyBluez_Win/
├── /ArduinoUNO/
├── /ArduinoMEGA2560/
├── /issues/
├── /comm/
├── /modules/
├── /docs/
├── ARCHITECTURE.md
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── ArduinoUNO.py
├── ArduinoMEGA2560.py
└── test_ArduinoUNO.py

```

### 开发的架构 

请阅读[ARCHITECTURE.md](https://github.com/Python4Embeded/Arduino/blob/main/ARCHITECTURE.md) 查阅为该项目的架构。

### 贡献者

请阅读**CONTRIBUTING.md** 查阅为该项目做出贡献的开发者。

#### 如何参与开源项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

### 作者

Dr. LI Shi <br />
python4embeded@gmail.com

 *您也可以在贡献者名单中参看所有参与该项目的开发者。*

### 版权说明

该项目签署了GPL 授权许可，详情请参阅 [LICENSE](https://github.com/python4embeded/arduino/blob/main/LICENSE)


<!-- links -->
[project-path]:python4embeded/arduino
[contributors-shield]: https://img.shields.io/github/contributors/python4embeded/arduino.svg?style=flat-square
[contributors-url]: https://github.com/python4embeded/arduino/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/python4embeded/arduino.svg?style=flat-square
[forks-url]: https://github.com/python4embeded/arduino/network/members
[stars-shield]: https://img.shields.io/github/stars/python4embeded/arduino.svg?style=flat-square
[stars-url]: https://github.com/python4embeded/arduino/stargazers
[issues-shield]: https://img.shields.io/github/issues/python4embeded/arduino.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/python4embeded/arduino.svg
[license-shield]: https://img.shields.io/github/license/python4embeded/arduino.svg?style=flat-square
[license-url]: https://github.com/python4embeded/arduino/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/leeshi
