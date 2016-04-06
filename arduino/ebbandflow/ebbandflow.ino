// Input pins
const int HUMIDITY_SENSOR_PIN = A1;


const int MANUAL_MODE = 0;
const int AUTOMATIC_MODE = 1;


// Output pins
const int PUMP_RELAY_PIN = 13;

float humidity_set_point = 0;
float solution_ph_set_point = 0;
float raw_humidity_value = 0;
float humidity_in_percent = 0;


int substrate_humidity_pump_status;

String command;

int system_mode;

void setup() {
  Serial.begin(115200);
  system_mode = AUTOMATIC_MODE;
  substrate_humidity_pump_status = LOW;
  pinMode(PUMP_RELAY_PIN, OUTPUT);
  digitalWrite(PUMP_RELAY_PIN, substrate_humidity_pump_status);
}

void loop() {
  raw_humidity_value = analogRead(HUMIDITY_SENSOR_PIN);
  float read_in_percent = 0.0;
  int scale = 735;
  humidity_in_percent = (raw_humidity_value / scale) * 100;
  Serial.print("{\"substrate_humidity\": "); Serial.print(humidity_in_percent); Serial.println("}");

  if(system_mode == AUTOMATIC_MODE) {
    if(humidity_in_percent < humidity_set_point) {
      digitalWrite(PUMP_RELAY_PIN, HIGH);
      Serial.println("{\"substrate_humidity_pump\": \"ON\"}");
    } else {
      digitalWrite(PUMP_RELAY_PIN, LOW);
      Serial.println("{\"substrate_humidity_pump\": \"OFF\"}");
    }
  }

  delay(30000);  // read each 30 seconds
}

void parse_command(String comm) {
  String subject;
  String value;
  int separator_idx;

  separator_idx = comm.indexOf('=');
  subject = comm.substring(0, separator_idx);
  value =  comm.substring(separator_idx + 1);

  Serial.println(comm);

  if(subject.equalsIgnoreCase("SYSTEM_MODE")) {
    system_mode = value.toInt();
    return;
  }

  if(subject.equalsIgnoreCase("SET_SUBSTRATE_HUMIDITY_SET_POINT")) {
    humidity_set_point = value.toFloat();
    Serial.print("{\"substrate_humidity_set_point\": "); Serial.print(value); Serial.println("}");
    return;
  }

  if(subject.equalsIgnoreCase("SET_SOLUTION_PH_SET_POINT")) {
    solution_ph_set_point = value.toFloat();
    Serial.print("{\"solution_ph_set_point\": "); Serial.print(value); Serial.println("}");
    return;
  }

  if(subject.equalsIgnoreCase("SUBSTRATE_HUMIDITY_PUMP")) {
    if(system_mode == MANUAL_MODE) {
      // Only change pump status if manual mode
      if(value == "ON") {
        digitalWrite(PUMP_RELAY_PIN, HIGH);
        Serial.println("{\"substrate_humidity_pump\": \"ON\"}");
      } else {
        digitalWrite(PUMP_RELAY_PIN, LOW);
        Serial.println("{\"substrate_humidity_pump\": \"OFF\"}");
      }
    }
  }
}

void serialEvent() {
  while (Serial.available()) {
    command = Serial.readStringUntil('\0');
    parse_command(command);
  }
}
