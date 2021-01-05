/*
  This shetch reads values from the Sensirion SGP30 VOC sensor and transmits it via MQTT
 It can be adabted to the ESP32 by using the AsynchMQTT Library example of the ESP32 and by filling in the needed sensor commands from this sketch
  
  It is based on the examples of the libraries

  Copyright: Andreas Spiess 2019

  Copyright: Andreas Spiess 2019
*/


#include <Wire.h>
#include <Adafruit_SGP30.h>


unsigned int eco2;
unsigned int tvoc;
char payloadStr[100];
unsigned long entryLoop, entryPublish;


Adafruit_SGP30 sgp;



uint32_t getAbsoluteHumidity(float temperature, float humidity) {
  // approximation formula from Sensirion SGP30 Driver Integration chapter 3.15
  const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
  const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity); // [mg/m^3]
  return absoluteHumidityScaled;
}



void setup()
{
  Serial.begin(115200);
  Serial.println("SGP30 test");

  if (! sgp.begin()) {
    Serial.println("Sensor not found :(");
    while (1);
  }
  Serial.print("Found SGP30 serial #");
  Serial.print(sgp.serialnumber[0], HEX);
  Serial.print(sgp.serialnumber[1], HEX);
  Serial.println(sgp.serialnumber[2], HEX);






  sgp.setHumidity(8200);  //8200 mg/m3 humidity (35% at 25 degrees

  // the first eco2 meaurements are always 400
  do {
    while (!sgp.IAQmeasure()) {
      Serial.print(".");
      delay(100);
    }
    tvoc = sgp.TVOC;
    Serial.print("TVOC(ppb):");
    Serial.print(tvoc);

    eco2 = sgp.eCO2;
    tvoc = sgp.TVOC;
    Serial.print(" eco2(ppm):");
    Serial.println(eco2);
    delay(1000);
  } while (eco2 == 400);
  entryLoop = millis();
}

void loop()
{
  static String payload;
  while (!sgp.IAQmeasure()) {
    Serial.print(".");
    delay(100);
  }

  tvoc = ((19 * tvoc) + sgp.TVOC) / 20;
  Serial.print("TVOC(ppb):");
  Serial.print(tvoc);

  eco2 = ((19 * eco2) + sgp.eCO2) / 20;
  Serial.print(" eco2(ppm):");
  Serial.print(eco2);


  while (!sgp.IAQmeasureRaw()) {
    Serial.print(".");
    delay(100);
  }
  unsigned int rawh2 = sgp.rawH2;
  Serial.print(" rawH2:");
  Serial.print(rawh2);

  unsigned int ethanol = sgp.rawEthanol;
  Serial.print(" Ethanol:");
  Serial.print(ethanol);

  Serial.print(" ");
  Serial.println((millis() - entryPublish) / 1000);

  if (millis() - entryPublish > 120000) {
    payload = "{\"tvoc\":" + String(tvoc) + ", \"eco2\":" + String(eco2) + ", \"rawh2\":" + String(rawh2) + ", \"ethanol\":" + String(ethanol) + "}";
    Serial.println(payload);
    payload.toCharArray(payloadStr, payload.length() + 1);
    entryPublish = millis();
  } 
  Serial.println();
  while (millis() - entryLoop < 1000) yield();
  entryLoop = millis();

}