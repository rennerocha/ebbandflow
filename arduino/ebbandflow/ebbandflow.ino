// Input pins
const int HUMIDITY_SENSOR_PIN = 1;

// Output pins
const int PUMP_RELAY_PIN = 5;

float humidity_set_point = 50;
float raw_humidity_value = 0;
float humidity_in_percent = 0;

void setup() {
  Serial.begin(9600);
  pinMode(PUMP_RELAY_PIN, OUTPUT);
  digitalWrite(PUMP_RELAY_PIN, LOW);
  Serial.println("pump_status=OFF");
}

void loop() {
  raw_humidity_value = analogRead(HUMIDITY_SENSOR_PIN);


  float read_in_percent = 0.0;
  int scale = 735;
  humidity_in_percent = (raw_humidity_value / scale) * 100;

//  humidity_in_percent = humidity_in_percent(raw_humidity_value);

  if(humidity_in_percent < humidity_set_point) {
    digitalWrite(PUMP_RELAY_PIN, HIGH);
    Serial.println("pump_status=ON");
  } else {
    digitalWrite(PUMP_RELAY_PIN, LOW);
    Serial.println("pump_status=OFF");
  }
  Serial.print("substrate_humidity=");
  Serial.println(humidity_in_percent);
  delay(30000);  // read each 30 seconds

  if(Serial.available()) {
    humidity_set_point = Serial.read() – '0';
  }
}
