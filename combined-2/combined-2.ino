int upPin = 12;      // blue push button
int downPin = 8;     // red push button
int modePin = 13;
int modeLED = 11;
int deployLED = 2;   // red
int retractLED = 3;  //green
int waitLED = 4;     //yellow

int pulPin = 9;                        
int dirPin = 10;
int myInt;
int myDump = 0;
long long variable = 0;
long long loops;

// Flags
int mode = 0;
int state = 2;

void setup() {
  Serial.begin(9600);
  pinMode(upPin, INPUT_PULLUP);
  pinMode(downPin, INPUT_PULLUP);
  pinMode(modePin, INPUT_PULLUP);
  pinMode(modeLED, OUTPUT);
  pinMode(waitLED, OUTPUT);
  pinMode(deployLED, OUTPUT);
  pinMode(retractLED, OUTPUT);
  
  pinMode(pulPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop(){
// ------ Mode Selection -------- 
   // Read the value of the input.
   // Button pressed gives a LOW value
   int modeValue = digitalRead(modePin);
   int downValue = digitalRead(downPin);
   int upValue = digitalRead(upPin);
   
   if (modeValue == LOW){
     // Manual mode
     mode = 1;
      digitalWrite(modeLED,LOW);
   }  else {
     // ML mode
     mode = 0;
      digitalWrite(modeLED, HIGH);
   }
   
// -------- Motor control -------- 
  if (mode == 0) {
    //Serial.println("ML mode entered");
    
    if (Serial.available() > 0){        //From RPi to Arduino
      myInt = (Serial.read() - '0');
     //conveting the value of chars to integer
      // Number of clicks per revolution = 5493;
//      variable = myInt*93381;

    }
    
    
    // Deploy
//    Serial.println(myInt);
    if (state == 2 && myInt == 1){
      Serial.println("ML says deploy");
      long long variable = 93381;
      digitalWrite(dirPin,HIGH);
      for (loops = 0; loops < variable; loops++) {
          digitalWrite(deployLED,HIGH);
          digitalWrite(retractLED,LOW);
          digitalWrite(waitLED,LOW);
          digitalWrite(pulPin, HIGH);
          delayMicroseconds(200);
          digitalWrite(pulPin, LOW);
          delayMicroseconds(200);
        }  
        state = 1;
        myInt = 0;
        loops = 0;
        digitalWrite(deployLED,LOW);
        
          //Serial.println("completed");
    }
    
    // Retract
    else if (state == 1 && myInt == 2)   {

      Serial.println("ML says retract");
      long long variable = 93381;
      digitalWrite(dirPin,LOW);
      for (loops = 0; loops < variable; loops++) {
          digitalWrite(retractLED,HIGH);
          digitalWrite(deployLED,LOW);
          digitalWrite(waitLED,LOW);
          digitalWrite(pulPin, HIGH);
          delayMicroseconds(200);
          digitalWrite(pulPin, LOW);
          delayMicroseconds(200);
        }    
        
         state = 2;
         myInt = 0;
         loops = 0;
         digitalWrite(retractLED,LOW);
         
    }
    
    else if (state == 1 && myInt == 1){
      digitalWrite(waitLED,HIGH);
      Serial.println("WDR Present, Already Deployed ");
      myInt = 0;
    }
    else if  (state == 2 && myInt == 2){
      digitalWrite(waitLED,HIGH);
      Serial.println("Blind already retracted");
      myInt = 0;
    }
    else{
      digitalWrite(waitLED,HIGH);
    }
  }
  
  
  if (mode == 1) {
    //Serial.println("Manual mode entered");
    if (Serial.available() > 0){         //From RPi to Arduino
      myDump = (Serial.read() - '0');
    }
    if (upValue == LOW && state == 1){
      //Serial.println("retract blinds");
      long long loops = 0;
      long long variable = 93381;
      digitalWrite(dirPin,LOW);
      for (loops = 0; loops < variable; loops++) {
        digitalWrite(retractLED,HIGH);
        digitalWrite(waitLED,LOW);
        digitalWrite(pulPin, HIGH);
        delayMicroseconds(200);
        digitalWrite(pulPin, LOW);
        delayMicroseconds(200);
      }  
      
      if (loops > 0 && loops == variable){
        digitalWrite(retractLED,LOW);
        loops = 0;
        variable = 0;
        state = 2;
        //Serial.println("completed");
      }
      
    }
    if (downValue == LOW && state == 2){
      //Serial.println("deploy blinds");
      long long loops = 0;
      long long variable = 93381;
      digitalWrite(dirPin,HIGH);
      for (loops = 0; loops < variable; loops++) {
        digitalWrite(deployLED,HIGH);
        digitalWrite(waitLED,LOW);
        digitalWrite(pulPin, HIGH);
        delayMicroseconds(200);
        digitalWrite(pulPin, LOW);
        delayMicroseconds(200);
      }  
      
      if (loops > 0 && loops == variable){
        digitalWrite(deployLED,LOW);
        loops = 0;
        variable = 0;
        state = 1;
        //Serial.println("completed");
      }
   }
   else {
     digitalWrite(waitLED,HIGH);
   }
  }
}
