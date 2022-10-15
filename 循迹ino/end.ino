#include <Servo.h>
Servo me1;//舵机1
Servo me2;//舵机2
int flag  = 0;//立标
const int TrigPin =12;
const int EchoPin = 11;
float cm;
void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  me1.attach(9);//舵机1数字输入引脚9
  me2.attach(5);//舵机2数字输入引脚10
  pinMode(6,INPUT);//引脚三用来读取右侧红外传感器参数
  pinMode(3,INPUT);
  pinMode(TrigPin,OUTPUT);
  pinMode(EchoPin,INPUT);
}
void goon(){
  //小车直行一小段
    me1.writeMicroseconds(2000);
    me2.writeMicroseconds(1000);
    delay(1200);
  }
void left(){
//小车左转
  me1.writeMicroseconds(1000);
  me2.writeMicroseconds(1000);
  delay(545);
}
void right(){
  //小车右转
    me1.writeMicroseconds(2000);
    me2.writeMicroseconds(2000);
    delay(570);
  }
void loop() {
    digitalWrite(TrigPin,LOW);
    delayMicroseconds(2);
    digitalWrite(TrigPin,HIGH);
    delayMicroseconds(10);
    digitalWrite(TrigPin,LOW);
    cm = pulseIn(EchoPin,HIGH)/58.0; 
    Serial.println(cm);
    if ((digitalRead(6)==0)&&(digitalRead(3)==0)){
      me1.writeMicroseconds(2000);
      me2.writeMicroseconds(1000);


      
      if((cm>2)&&(cm<7)){
      flag = 1;
      }
    if(flag==1){
      right();
      goon();
      left();
      goon();
      delay(300);
      goon();
      left();
      goon();
      right();
      flag = 0;
      }
    }
  else if ((digitalRead(6)==0)&&(digitalRead(3)==1)){

    me1.writeMicroseconds(1000);
    me2.writeMicroseconds(1000);
  }
  else if ((digitalRead(6)==1)&&(digitalRead(3)==0)){
    //偏离轨道

    me1.writeMicroseconds(2000);
    me2.writeMicroseconds(2000);
  }
  else{
    //十字路口正常行驶
    me1.writeMicroseconds(2000);
    me2.writeMicroseconds(1000);
    }
    


}
