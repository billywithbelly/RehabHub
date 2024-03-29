#include <WiFi.h>
#include <WiFiUdp.h>

typedef enum {
  IDLE,
  LIGHTSUP,
} Status;

const char WIFI_SSID[]="UCInet Mobile Access";
const char WIFI_PASSWORD[]="";
const int LEDPIN=2;
const int SENSORPIN=15;
const int SENSORWINDOW=50;
const int ESPID=2;

WiFiUDP Udp;
IPAddress remoteIp;
unsigned int UDPPort=8888;

unsigned long reflectTime=millis();
unsigned long blink10Sec=millis();
int sensorStart=0;

Status LEDStatus=IDLE;
char packetBuffer[32];
int record=0;
bool recordBlink=false;

void udp_send(char* data);

void setup() {
  Serial.begin(115200);
  delay(1000);
  pinMode(LEDPIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID); 
  while (WiFi.status() != WL_CONNECTED) {
        Serial.print("...");
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD); 
        delay(5000);
    }
    Serial.println("\nWi-Fi Connected");

  Serial.println("\nIP obtained: " + WiFi.localIP().toString());
  Udp.begin(UDPPort);
  delay(1000);
}

void loop() {
  // Waiting for Pi commands
  if (Udp.parsePacket()) {
    remoteIp = Udp.remoteIP();
    Serial.print("Received packet from IP <"); Serial.print(remoteIp);
    Serial.print(":"); Serial.print(Udp.remotePort()); Serial.println(">");
    
    // Read the packet content
    int packetLength = Udp.read(packetBuffer, sizeof(packetBuffer));
    if (packetLength > 0) {
      packetBuffer[packetLength] = '\0';
    }
    Serial.print("Message received: "); Serial.println(packetBuffer);


    // Packet format: #RL
    // Packet Sample: #01
    if (packetBuffer[0]=='#') { // Light up led
      if (packetBuffer[ESPID]=='1') {
        Serial.println("Start testing");
        // First get the initial brightness value
        sensorStart = analogRead(SENSORPIN);
        Serial.print("Starting brightness: "); Serial.println(sensorStart);
        reflectTime=millis();
        LEDStatus = LIGHTSUP;
      }
    }

    // Packet sample: *L1
    else if (packetBuffer[0]=='*') {
      if (packetBuffer[1]=='L' && packetBuffer[2]=='1') {
        Serial.println("Personal Record!");
        record=1;
        blink10Sec=millis();
      }
    }
  }

  if (LEDStatus==LIGHTSUP) {
    int sensorValue = analogRead(SENSORPIN);
    if ((sensorStart - sensorValue) >= SENSORWINDOW) {
      // Reply the result to the Raspberry Pi
      char udpBuffer[128];
      snprintf(udpBuffer, sizeof(udpBuffer), "%c%02d", (ESPID==1?'R':'L'), (millis()-reflectTime)/1000);
      udp_send(udpBuffer);
      LEDStatus = IDLE;
    }
  }

  if (record != 0) {
    if ((millis() - blink10Sec) >= 300) { // Blink every 0.3 seconds
      recordBlink =! recordBlink;
      digitalWrite(LED_BUILTIN, recordBlink);
      record++;
      blink10Sec = millis();
    }
    if (record >= 20) {
      record = 0;
      recordBlink = false;
      digitalWrite(LED_BUILTIN, false);
    }
  }
}

void udp_send(char* data){
  int i;
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Serial.println(data);
  while (data[i] != '\0') Udp.write((uint8_t)data[i++]);
  Udp.endPacket();
}
