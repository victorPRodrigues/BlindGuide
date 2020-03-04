#include <NewPing.h>

// Global Constants
#define sensorNum    4 
#define maxDistance  400
#define pingInterval 15
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
void motorsResponse();
void bridgeControl(uint8_t pin, bool state); 

void setup() {
  Serial.begin(115200);
  pinMode(clockPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(enable, OUTPUT);
  
  pingTimer[0] = millis() + 75;           
  for (uint8_t i = 0; i < sensorNum; i++) {
    pingTimer[i] = (i == 0) ? millis() + 75 : pingTimer[i - 1] + pingInterval;
    pinMode(motorsPWM[i], OUTPUT);
    pinMode(hBridgeA[i], OUTPUT);
    pinMode(hBridgeB[i], OUTPUT);
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

void motorReaction() {
  for(uint8_t i = 0; i < sensorNum; i++) {
    if(sensor[currentSensor].check_timer()) {
      bridgeControl(hBridgeA[i], HIGH);
      bridgeControl(hBridgeB[i], LOW);
      unsigned int distance_CM = (sensor[currentSensor].ping_result / US_ROUNDTRIP_CM);
      float distance = distance_CM / 100;
      if(distance == 0.0)
        distance = 4;

      distance = map(distance, 0.5, 4, 255, 0);  
      analogWrite(motorsPWM[i], distance);
    } else {
      bridgeControl(hBridgeA[i], LOW);
      bridgeControl(hBridgeB[i], LOW);
    }
        
  }
}

void bridgeControl(uint8_t pin, bool state) {
  static uint8_t bridgeBuffer;
  bitWrite(bridgeBuffer, pin%8, state);

  digitalWrite(latchPin, LOW);
  digitalWrite(dataPin, LOW);
  
  for (int b = 0; b < 8; b++) {
    digitalWrite(clockPin, LOW);        
    digitalWrite(dataPin,  bitRead(bridgeBuffer, b) );
    
    digitalWrite(clockPin, HIGH); 
    digitalWrite(dataPin, LOW);     
  }  
}
