#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h> 


Servo myservo;  // create servo object to control a servo 

// assign a MAC address for the ethernet controller.
// fill in your address here:
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};

// initialize the library instance:
EthernetClient client;

char server[] = "http://2.1lock.sinaapp.com";

unsigned long lastConnectionTime = 0;             // last time you connected to the server, in milliseconds
const unsigned long postingInterval = 3L * 1000L; // delay between updates, in milliseconds
// the "L" is needed to use long type numbers


#define PINUNLOCK 4
#define PINLOCK 3
#define PINLED 2
boolean IsLock = true;
boolean HaveSendState = true;
unsigned long lastLockTime = 0;


void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(30);

  pinMode(PINLED, OUTPUT);
  pinMode(PINUNLOCK, INPUT);
  pinMode(PINLOCK, INPUT);
  
  // start serial port:
  Serial.begin(9600);
//  while (!Serial) {
//    ; // wait for serial port to connect. Needed for Leonardo only
//  }

  // give the ethernet module time to boot up:
  delay(1000);
  // start the Ethernet connection using a fixed IP address and DNS server:
  Ethernet.begin(mac);
  // print the Ethernet board/shield's IP address:
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());
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
    Serial.write(c);
    if (c == '0'){
      unlock();
    }
//    else if(c == '1'){
//      lock();
//    }
  }

  // if ten seconds have passed since your last connection,
  // then connect again and send data:
  if ((millis() - lastConnectionTime > postingInterval) && (millis() - lastLockTime > postingInterval)) {
    if(HaveSendState && IsLock)
      httpRequest(2);
    else if(!HaveSendState)
      sendLockState();
  }

}

// this method makes a HTTP connection to the server:
void httpRequest(int cmd) {
  // close any connection before send a new request.
  // This will free the socket on the WiFi shield
  client.stop();

  // if there's a successful connection:
  if (client.connect(server, 80)) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    if (cmd == 2)
      client.println("GET http://2.1lock.sinaapp.com/lockstate?lockticket=gQHj7zoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xLzRFakNwTkhsdnNuSHdVQkdNR1FkAAIENmrhVAMEAAAAAA==&lockadmin=o2dlOs61G3vUWMsJ5Cimh7s-MPkQ&updata=2");
    else if(cmd == 1)
      client.println("GET http://2.1lock.sinaapp.com/lockstate?lockticket=gQHj7zoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xLzRFakNwTkhsdnNuSHdVQkdNR1FkAAIENmrhVAMEAAAAAA==&lockadmin=o2dlOs61G3vUWMsJ5Cimh7s-MPkQ&updata=1");
    else if(cmd == 0)
      client.println("GET http://2.1lock.sinaapp.com/lockstate?lockticket=gQHj7zoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xLzRFakNwTkhsdnNuSHdVQkdNR1FkAAIENmrhVAMEAAAAAA==&lockadmin=o2dlOs61G3vUWMsJ5Cimh7s-MPkQ&updata=0");
    client.println("Host: http://2.1lock.sinaapp.com");
    client.println("User-Agent: arduino-ethernet");
    client.println("Connection: close");
    client.println();

    // note the time that the connection was made:
    lastConnectionTime = millis();
  }
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
  }
}

void unlock(void){
  digitalWrite(PINLED, HIGH);
  myservo.write(30);
  IsLock = false;
  lastLockTime = millis();
  HaveSendState = false;
  delay(1500);
}

void lock(void){  
  digitalWrite(PINLED, LOW);
  myservo.write(120);
  IsLock = true;
  lastLockTime = millis();
  HaveSendState = false;
}

int sendLockState(void)
{
  if(IsLock)
    httpRequest(1);
  else
    httpRequest(0);
  HaveSendState = true;
}
