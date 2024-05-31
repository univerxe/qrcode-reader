int IN1 = 6;
int IN2 = 7;
int IN3 = 8;
int IN4 = 9;

void setup() {
  Serial.begin(9600);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  stop();
  Serial.begin(9600); 

  // moveForward(); 
  // delay(2000);
  // stop();
  // backward(); 
  // delay(2000);
  // stop();

  // moveLeft(); 
  // delay(2000);
  // stop();

  // moveRight(); 
  // delay(2000);
  // stop();

}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "left") {
      moveLeft();
    } else if (command == "right") {
      moveRight();
    } else if (command == "forward") {
      moveForward();
    } else {
      stop();
    }
  }
}

void moveLeft(){
  digitalWrite(IN2, LOW);
  digitalWrite(IN4, LOW);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN3, HIGH);
}

void backward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN4, HIGH);
}

void moveForward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN4, LOW);
}

void moveRight(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN4, HIGH);
}

void stop(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}