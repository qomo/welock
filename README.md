# Welock

Welock是一个微信门锁  
基本想法是通过手机微信扫描门锁上的二维码实现开门的功能  
基本结构：门锁 <<===>> SAE <<===>> 微信测试号

门锁用Arduino＋网络模块与SAE服务器通信，接收开锁命令。  
SAE服务器同时作为微信测试号的接口服务器，用于响应服务号的请求。

## Arduino虚拟串口测试ESP2866
目录：/test_esp2866  
这是一个Arduino的虚拟串口程序，直接来源于Arduino的示例程序  
它实现一个功能：将Arduino串口与虚拟串口之间的信息互换  
ESP2866 与 Arduino的连线规则：  
VCC   <<--->> 3.3V  
CH_PD <<--->> 3.3V  
GND	  <<--->> GND  
UTXD  <<--->> D11  
URXD  <<--->> D10  

具体关于ESP8266的测试命令，还可以参考：
> http://rancidbacon.com/files/kiwicon8/ESP8266_WiFi_Module_Quick_Start_Guide_v_1.0.4.pdf

NOTE：这个方式同样适用于测试其他串口通信的外围硬件，如蓝牙模块

## Arduino Ethernet Shield ＋ Yeelink
目录：/yeelink_demo  
这是用Arduino Ethernet Shield网络模块与Yeelink平台实现的welock demo  
*硬件部分*，一个LED灯暂时模拟控制门锁的舵机  
一个开关（这里用的是触动开关）用于获取门的状态（开／关）。当把门合起时，自动获取关门动作  
另一个开关用做本地开门的动作，置于门内侧  

另一个开门动作由微信触发，用作门外开门（基本已经完成，待与yeelink连接）  
**Note:** 后来发现，SAE不好对yeelink发送http请求，于是放弃yeelink，让Arduino硬件直接与SAE通信

*使用场景介绍：*  
假如要从外面开门进入室内，需要用微信扫描门锁上的二维码，微信给SAE服务器发送响应指令，SAE向yeelink发送开门指令，Arduino轮训yeelink上的开门指令获得开门指令，实施开门  
进入室内后，用手将门合上，自动触发门锁上的关门开关，Arduino执行关门动作，向yeelink更新门闭合的状态。  
若要从室内开门，直接按门内侧上的开门按钮，Arduino执行开门动作，向yeelink更新门开启的状态。  
出到室外后，用手带上门，自动触发门锁上的关门开关……  

> 接下来需要做一些真正的模型

## 看起来还不错的demo——第一个版本
这是第一个稳定版本，如最初的构想，只用Arduino＋SAE＋微信测试号。不需要yeelink。  
SAE服务器代码：/1lock （使用的是第二个版本）  
Arduino代码：/welock_sae_demo  

使用体验如"Arduino Ethernet Shield ＋ Yeelink"中所述  
只是去处了yeelink这个云平台，成最简单的“Arduino门锁 <<===>> SAE <<===>> 微信测试号”结构  

## 联系我
如果你对这个项目感兴趣，可以与我交流：  
Email：qomoliao@gmail.com  
微信：qomoliao  
或许你也对我个人的Blog感兴趣：qomo.sinaapp.com  
