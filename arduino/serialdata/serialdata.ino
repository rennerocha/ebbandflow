#include "DHT.h"

#define DHTTYPE DHT11
const int DHTPIN = 9;
DHT dht(DHTPIN, DHTTYPE);

const long READ_INTERVAL = 0.5;  // interval between sensors reading (in minutes)
long previousMillis = 0; // will store last time the read interval was executed

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);           // set up Serial library at 9600 bps
  dht.begin();
}

void loop() {
//    unsigned long currentMillis = millis();
//    if(currentMillis - previousMillis > READ_INTERVAL * 1000 * 60) {
      float h = dht.readHumidity();
      // Read temperature as Celsius (the default)
      float t = dht.readTemperature();

      Serial.print("");
      Serial.print("humidity=");
      Serial.print(h);
      Serial.print("&temperature=");
      Serial.println(t);
//      previousMillis = currentMillis;
delay(2000);
//    }
}
