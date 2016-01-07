
int counter = 1000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);           // set up Serial library at 9600 bps
}

void loop() {
  Serial.println(counter);  // prints hello with ending line break 
  counter = counter + 1;
  delay(500);
}
