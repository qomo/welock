# Welock

Welock是一个微信门锁  
基本想法是通过手机微信扫描门锁上的二维码实现开门的功能  
基本结构：门锁 <<===>> SAE <<===>> 微信测试号

门锁用Arduino＋ESP2866 Wi-Fi模块与SAE服务器通信，接收开锁命令。  
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