#include <SoftwareSerial.h>
SoftwareSerial hc06(2, 3);
const int LED1 = 10;
const int LED2 = 11;
void setup() {
    Serial.begin(9600);
    hc06.begin(9600);
    pinMode(LED1, OUTPUT);
    pinMode(LED2, OUTPUT);
}
void loop() {
    if(hc06.available()){
        char message = (char)hc06.read();
        if(message=='1'){
            digitalWrite(LED1, HIGH);
            digitalWrite(LED2, LOW);
        }
        else if(message=='2'){
            digitalWrite(LED1, LOW);
            digitalWrite(LED2, HIGH);
        } 
    }
    if(Serial.available()){
        hc06.write(Serial.read());
    }
}
