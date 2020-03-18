#include <NewPing.h>

// Global Constants
#define sensorNum    4 
#define maxDistance  400
#define pingInterval 30
const uint8_t hBridgeA[sensorNum]  = {  2, 1, 5, 0 };
const uint8_t hBridgeB[sensorNum]  = {  3, 4, 7, 6  };

// Global Variables
unsigned long pingTimer[sensorNum];
uint8_t       currentSensor = 0;

// Pinout
#define clockPin  4
#define dataPin   8
#define enable    7
#define latchPin  12
const uint8_t motorsPWM[sensorNum] = { 11, 3, 5, 6 };
NewPing sensor[sensorNum] = {
  NewPing(22, 24, maxDistance), //Trigger, Echo
  NewPing(28, 30, maxDistance),
  NewPing(34, 36, maxDistance),
  NewPing(40, 42, maxDistance),
};

// Auxiliar Functions
void bridgeControl(uint8_t pin, bool state);
void motorsResponse();

void setup() {
  Serial.begin(115200);
  pinMode(clockPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(enable, OUTPUT); 
  digitalWrite(enable, LOW);
  
  pingTimer[0] = millis() + 75;
  for (uint8_t i = 0; i < sensorNum; i++) {
    if (i != 0)
      pingTimer[i] = pingTimer[i - 1] + pingInterval; 
      
    pinMode(motorsPWM[i], OUTPUT);
    pinMode(hBridgeA[i], OUTPUT);
    pinMode(hBridgeB[i], OUTPUT);
    bridgeControl(hBridgeA[i], HIGH);
    bridgeControl(hBridgeB[i], LOW);
  }
}

void loop() {
  for (uint8_t i = 0; i < sensorNum; i++) { 
    if (millis() >= pingTimer[i]) {         
      pingTimer[i] += pingInterval * sensorNum;  
      sensor[currentSensor].timer_stop();          
      currentSensor = i;                          
      sensor[currentSensor].ping_timer(motorReaction);
    }
  }
}

void bridgeControl(uint8_t pin, bool state) {
  static byte bridgeBuffer[1];
  bitWrite(bridgeBuffer[pin / 8], pin % 8, state);
  
  digitalWrite(latchPin, LOW); 
  digitalWrite(dataPin, LOW);  
  digitalWrite(clockPin, LOW);

  for (int nB = 7; nB >= 0; nB--) {
    digitalWrite(clockPin, LOW);  
    digitalWrite(dataPin,  bitRead(bridgeBuffer[1], nB));
    digitalWrite(clockPin, HIGH); 
    digitalWrite(dataPin, LOW);     
  }  
  
  digitalWrite(latchPin, HIGH);  
} 



void motorReaction() {
  if(sensor[currentSensor].check_timer()) {
    float distance_CM = (sensor[currentSensor].ping_result / US_ROUNDTRIP_CM);
    float distance = distance_CM / 100;
    if(distance == 0.0)
      distance = 4;
       
    distance = map(distance, 0.2, 4, 255, 0);  

    bridgeControl(hBridgeA[currentSensor], HIGH);
    bridgeControl(hBridgeB[currentSensor], LOW);  
    analogWrite(motorsPWM[currentSensor], distance);
  }
}
