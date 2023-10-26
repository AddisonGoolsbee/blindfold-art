#include <WiFi.h>
#include <WiFiUdp.h>
#include <math.h>

const int pin = 34; 

const char* ssid = "yale wireless";

const char* udpServerIP = "172.27.33.77"; 
const int udpServerPort = 12345; 

WiFiUDP udp;


double angle = 0.0;
double increment = 0.01;

void setup() {
  pinMode(pin, INPUT);
  Serial.begin(115200); 

  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  udp.begin(udpServerPort);
}

void loop() {
  double pitch = sin(angle);
  double yaw = cos(angle);
  angle += increment;

  char buffer[50];
  sprintf(buffer, "Pitch: %.2f, Yaw: %.2f", pitch, yaw);

  Serial.println(buffer);
  udp.beginPacket(udpServerIP, udpServerPort);
  udp.println(buffer);
  udp.endPacket();

  delay(5);


}


