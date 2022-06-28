/* Server in ArduinoUNO
 by Python for Arudino UNO <https://github.com/Python4Embeded>
 This server code is in the public domain.

 modified 1 Jun 2022
 by LI Shi
 https://github.com/Python4Embeded/ArduinoUNO
*/
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <Servo.h>

#define digitalPin_Sum 14   //total number of digital pin
#define analogPin_Sum 6    //total number of analog pin

#define mySerialPin_RX 7    // customer defined the software serial rx pin
#define mySerialPin_TX 8    // customer defined the software serial tx pin

Servo myservo; // create servo object to control a servo
// twelve servo objects can be created on most boards

SoftwareSerial mySerial(mySerialPin_RX, mySerialPin_TX);  // customer defined the software serial

String recvStr = "";      // variable to store the receive string from software serial

DynamicJsonDocument recvMsg_doc(300);     // create JsonDocument object to transfer receive string to Json Document
StaticJsonDocument<300> sndMsg_doc;       // create JsonDocument object to store the message sending through software serial
JsonArray analogValues;     // create JsonArray object to store the value of analog pin on UNO board
JsonArray digitalValues;    // create JsonArray object to store the value of digital pin on UNO board

bool recvAck;     // variable to decide receiving the software serial message or not 
uint8_t pinValue[14];   //variable to store the digital pin value
uint8_t servoPin;    // variable to store the servo pin
bool hasServo;    // variable to decide connecting the servo or not

// Function: read the pin value
bool get_pinRead(void);

// Function: refresh the port on UNO board with the variable of pinValue
bool refresh_pinWrite(void);

// Function: update the digital port of UNO board with the receiving message from software serial 
bool update_pinWrite(void);

// Function: update the status of servo connected to UNO board with the receiving message from software serial 
bool update_servo(void);

// Function: send message to software serial
bool sndAck_message(void);

// Function: analysis the message receiving from software serial
bool analysis_message(void);

void setup() {
  // put your setup code here, to run once:
  mySerial.begin(9600);   //set up software serial library baud rate to 9600
  Serial.begin(9600);   //set up serial library baud rate to 9600
  recvAck = false;
  hasServo = false;
  servoPin = 9;   // set up default servo pin to 9
  
  for (int i = 0; i < sizeof(pinValue); i ++)
  {
      if (i == mySerialPin_RX) continue;
      if (i == mySerialPin_TX) continue;
      pinValue[i] = 0;  
  }
  
  while (!mySerial) continue;
  while (!Serial) continue;
  
  Serial.println(F("Server is ready."));
  Serial.println(F("Please connect..."));
}

void loop() {
   // put your main code here, to run repeatedly:
   // received the message and saved to recvStr
   while (mySerial.available())
   {
      char c = char(mySerial.read());
      if(c != '*') {
        recvStr += c;
      } else {
        recvAck = true;
      } 
   } 

  // if received the software serial message successed
   if(recvAck)
   {
      delay(100);
      if (recvStr.length() > 0)
      {
        analysis_message();  // analysis the message from software serial and to execute
      } else {
        sndAck_message();   // read the current pin value and send to software serial
      }

      recvStr = "";
      recvAck = false;
      recvMsg_doc.clear();
      sndMsg_doc.clear();
   }

   refresh_pinWrite();
}

bool sndAck_message(void)
{
  bool res = get_pinRead();   // read the pin value   
  serializeJson(sndMsg_doc, mySerial);    // send the message to software serial
  serializeJson(sndMsg_doc, Serial);    // send the message to serial for monitor
  Serial.print("\n");

  return res;
}

bool analysis_message(void)
{
  bool res;
  
  DeserializationError error = deserializeJson(recvMsg_doc, recvStr);
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return false;
  }
  //upadte the board port value or servo status by recvieve message
  if(recvMsg_doc["HD"]== "Arduino_UNO")
      res = update_pinWrite();
  else if (recvMsg_doc["HD"] == "servo")
      res = update_servo();
      
  return res;
}

bool update_servo(void)
{   
  if(recvMsg_doc["number"] == 1)
  {
      servoPin = recvMsg_doc["pin_no"];   //set the servo Pin
      Serial.println("Servo attached!");
      
      if (recvMsg_doc["pos"] == 0) 
      {
        hasServo = true;
        myservo.attach(recvMsg_doc["pin_no"]);    //attach the servo
      }
      else { 
        myservo.write(recvMsg_doc["pos"]);   //set the servo turning to the pos     
      }
  }
  else if (recvMsg_doc["number"] == 0)
  {
      hasServo = false;
      Serial.println("Servo detached!");
      myservo.detach();
  }

}

bool refresh_pinWrite(void)
{ 
  //update the digital and analog port Value in board with the pinValue list.
  for (int pin = 0; pin < digitalPin_Sum; pin++) {
      // Write the digital output
      if (pin == mySerialPin_RX) continue;
      if (pin == mySerialPin_TX) continue;
      if (hasServo && pin == servoPin) continue;
      if (pinValue[pin] < 2)
        digitalWrite(pin, pinValue[pin]);
      else
        analogWrite(pin, pinValue[pin]);
  }
  
  return true;  
}

bool update_pinWrite(void)
{
  //update the pin value by the recvieve message 
  for (int pin = 0; pin < digitalPin_Sum; pin++) {
      // Write the digital output
        pinValue[pin] =  recvMsg_doc["digital"][pin];
  }
  return true;  
}

bool get_pinRead(void)
{
  analogValues = sndMsg_doc.createNestedArray("analog");
  digitalValues = sndMsg_doc.createNestedArray("digital");
  
  for (int pin = 0; pin < analogPin_Sum; pin++) {
  // Read the analog input
    int value = analogRead(pin);
  // Add the value at the end of the array
    analogValues.add(value);
  }      
  
  for (int pin = 0; pin < digitalPin_Sum; pin++) {
  // Read the digital input
    int value = digitalRead(pin);
  // Add the value at the end of the array
    digitalValues.add(value);
  }   
  return true;
}
