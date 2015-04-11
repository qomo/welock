/*
 Yeelink sensor client power switch example
 */

#include <SPI.h>
#include <Ethernet.h>
#include <Wire.h>
#include <math.h>
#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
byte buff[2];

// for yeelink api
#define APIKEY         "56a0a6abac1515d8fba7b65d170fd0d3" // 此处替换为你自己的API KEY
#define DEVICEID       19669 // 此处替换为你的设备编号
#define SENSORID       34503 // 此处替换为你的传感器编号

// assign a MAC address for the ethernet controller.
byte mac[] = { 0x00, 0x1D, 0x72, 0x82, 0x35, 0x9D};
// initialize the library instance:
EthernetClient client ;
char server[] = "api.yeelink.net";   // name address for yeelink API

unsigned long lastConnectionTime = 0;          // last time you connected to the server, in milliseconds
boolean lastConnected = false;                 // state of the connection last time through the main loop
const unsigned long postingInterval = 5*1000; // delay between 2 datapoints, 30s
String returnValue = ""; 
boolean ResponseBegin = false;
unsigned long lastLockTime = 0;

#define PINUNLOCK 4
#define PINLOCK 3
boolean IsLock = false;
boolean HaveSendState = false;

void setup() {
  pinMode(2, OUTPUT);
  pinMode(PINUNLOCK, INPUT);
  pinMode(PINLOCK, INPUT);
  Wire.begin();
  // start serial port:
 Serial.begin(9600);
      myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  // start the Ethernet connection with DHCP:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    for(;;)
      ;
  }
  else {
    Serial.println("Ethernet configuration OK");
  }
}

void loop() {
  if(IsLock && digitalRead(PINUNLOCK)){
    delay(100);
    if(IsLock && digitalRead(PINUNLOCK)){
      unlock();
    }
  }
  if(!IsLock && digitalRead(PINLOCK)){
    delay(100);
    if(!IsLock && digitalRead(PINLOCK)){
      lock();
    }
  }
  
  
  // if there's incoming data from the net connection.
  // send it out the serial port.  This is for debugging
  // purposes only:

  if (client.available()) {
    char c = client.read();
    Serial.print(c);
      if (c == '{')
        ResponseBegin = true;
      else if (c == '}')
        ResponseBegin = false;

      if (ResponseBegin)
        returnValue += c;   
  }
  
  if (returnValue.length() !=0 && (ResponseBegin == false))
  {
//    Serial.println(returnValue);
    if (returnValue.charAt(returnValue.length() - 1) == '1') {
      Serial.println("turn on the LED"); 
      unlock();
    }
     returnValue = "";
  }
  
  
  // if there's no net connection, but there was one last time
  // through the loop, then stop the client:
  if (!client.connected() && lastConnected) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
  
  // if you're not connected, and ten seconds have passed since
  // your last connection, then connect again and send data:
  if(!client.connected() && (millis() - lastConnectionTime > postingInterval) && (millis() - lastLockTime > postingInterval)) {
    // read sensor data, replace with your code
    //int sensorReading = readLightSensor();
    Serial.print("yeelink:");
    if(HaveSendState)
      //get data from server  
      getData();
    else
      sendLockState();
  }
  // store the state of the connection for next time through
  // the loop:

  lastConnected = client.connected();
}

void unlock(void){
  digitalWrite(2, HIGH);
  IsLock = false;
  lastLockTime = millis();
  HaveSendState = false;
  delay(1500);
}

void lock(void){  
  digitalWrite(2, LOW);
  IsLock = true;
  lastLockTime = millis();
  HaveSendState = false;
}

int sendLockState(void)
{
  if(IsLock)
    sendData(0);
  else
    sendData(1);
  HaveSendState = true;
}

// this method makes a HTTP connection to the server and get data back
void getData(void) {
  // if there's a successful connection:
  if (client.connect(server, 80)) {
    Serial.println("connecting...");
    // send the HTTP GET request:
    
    client.print("GET /v1.0/device/");
    client.print(DEVICEID);
    client.print("/sensor/");
    client.print(SENSORID);
    client.print("/datapoints");
    client.println(" HTTP/1.1");
    client.println("Host: api.yeelink.net");
    client.print("Accept: *");
    client.print("/");
    client.println("*");
    client.print("U-ApiKey: ");
    client.println(APIKEY);
    client.println("Content-Length: 0");
    client.println("Connection: close");
    client.println();
    Serial.println("print get done.");
    
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
   // note the time that the connection was made or attempted:
  lastConnectionTime = millis();
}

// this method makes a HTTP connection to the server:
void sendData(int thisData) {
  // if there's a successful connection:
  if (client.connect(server, 80)) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.print("POST /v1.0/device/");
    client.print(DEVICEID);
    client.print("/sensor/");
    client.print(SENSORID);
    client.print("/datapoints");
    client.println(" HTTP/1.1");
    client.println("Host: api.yeelink.net");
    client.print("Accept: *");
    client.print("/");
    client.println("*");
    client.print("U-ApiKey: ");
    client.println(APIKEY);
    client.print("Content-Length: ");

    // calculate the length of the sensor reading in bytes:
    // 8 bytes for {"value":} + number of digits of the data:
    int thisLength = 10 + getLength(thisData);
    client.println(thisLength);
    
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Connection: close");
    client.println();

    // here's the actual content of the PUT request:
    client.print("{\"value\":");
    client.print(thisData);
    client.println("}");
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
   // note the time that the connection was made or attempted:
  lastConnectionTime = millis();
}


// This method calculates the number of digits in the
// sensor reading.  Since each digit of the ASCII decimal
// representation is a byte, the number of digits equals
// the number of bytes:
int getLength(int someValue) {
  // there's at least one byte:
  int digits = 1;
  // continually divide the value by ten, 
  // adding one to the digit count for each
  // time you divide, until you're at 0:
  int dividend = someValue /10;
  while (dividend > 0) {
    dividend = dividend /10;
    digits++;
  }
  // return the number of digits:
  return digits;
}
