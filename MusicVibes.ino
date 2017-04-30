#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int inByte = 0;         // incoming serial byte
int nextByte = 0;
int mode = 0;
int motors[8];
int motor_high = 4095;
int motor_low = 1024;
int power = 256;
uint8_t servonum = 0;
//int vibrate = 0;

void setup() {
  int i;
  for(i=0; i<8; i++){
    motors[i] = 0;
  }
  // start serial port at 9600 bps and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  //pinMode( 6 , OUTPUT);
  pwm.begin();
  pwm.setPWMFreq(1000);
  for(servonum=0; servonum<8; servonum++){
    pwm.setPWM(servonum, 0, 0);
  }
  //establishContact();  // send a byte to establish contact until receiver responds
}

void vibrate_on_byte(int byte){
  if(byte!=-1){
    int bit_testing;
    unsigned char my_char = (unsigned char)byte;
    for(bit_testing =0; bit_testing<8; bit_testing++){
      if(my_char&0x01){
        analogWrite( 6 , 153 );
        delay(500);
        analogWrite( 6 , 0 );
      } else {
        delay(500);
      }
      my_char = my_char >> 1;
      delay(125);
    }
  }
}

void set_motors(int a_mode, int byte){
  if(byte!=-1){
    int bit_testing;
    unsigned char my_char = (unsigned char)byte;
    for(bit_testing =0; bit_testing<8; bit_testing++){
      if(my_char&0x01){
        switch(a_mode){
          case 0: // Set High
            motors[7-bit_testing] = motor_high;
            break;
          case 1: // Set Low
            if(motors[7-bit_testing]<motor_low){
              motors[7-bit_testing] = motor_low;
            }
            break;
          case 2: // Clear & High
            motors[7-bit_testing] = motor_high;
            break;
          default:
            break;
        }
      } else {
        if(a_mode == 2){
          motors[7-bit_testing] = 0;        
        }
      }
      my_char = my_char >> 1;
    }
  }
}

void vibrate_seat(){
  int i;
  for(i=0; i<8; i++){
    pwm.setPWM(i, 0, motors[i]);
  }
}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    mode = Serial.read();
    switch(mode){
    case 0:
      //2 at a time
      inByte = nextByte;
      nextByte = Serial.read();
      set_motors(2, inByte);
      set_motors(1, nextByte);
      break;
    case 1:
      // One at a time
      inByte = Serial.read();
      nextByte = 0;
      set_motors(2, inByte);
      break;
    case 2:
      //init for 2 at a time
      inByte = Serial.read();
      nextByte = Serial.read();
      set_motors(2, inByte);
      set_motors(1, nextByte);
      break;
    case 3:
	  //set lower
      nextByte = Serial.read();
      set_motors(1, nextByte);
      break;
    case 4:
      //Settings
      power = Serial.read();
      power++;
      motor_high = power*16;
      motor_low = power*4;
      if(motor_high>4095){
        motor_high = 4095;
      }
      set_motors(2, inByte);
      set_motors(1, nextByte);
      break;
    default:
      break;
    }
    //vibrate_on_byte(inByte);
    vibrate_seat();
    //Serial.println((char)inByte);
  }
  
}

/*void establishContact() {
  while (Serial.available() <= 0) {
    Serial.println("0,0,0");   // send an initial string
    delay(300);
  }
}*/