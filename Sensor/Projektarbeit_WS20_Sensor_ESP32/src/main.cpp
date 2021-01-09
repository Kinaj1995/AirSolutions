/**
 * WiFiManager advanced demo, contains advanced configurartion options
 * Implements TRIGGEN_PIN button press, press for ondemand configportal, hold for 3 seconds for reset settings.
 */

//--Libaries
#include <Arduino.h>
#include <ArduinoOTA.h>

//--Other-Files
#include <settings.h>
#include <file.h>
#include <network.h>
#include <sensor.h>
#include <ntp.h>




//--Taskhandler
TaskHandle_t Core0;
void LoopCore0(void *pvParameters);

//--Functions

void setup()
{
  //Create Task for Core0
  xTaskCreatePinnedToCore(
      LoopCore0, /* Task function. */
      "Cor0",    /* name of task. */
      10000,     /* Stack size of task */
      NULL,      /* parameter of the task */
      1,         /* priority of the task */
      &Core0,    /* Task handle to keep track of created task */
      0);        /* pin task to core 0 */
  delay(500);

  Serial.begin(115200);

  loadSPIFFS(); //Initialize the Local Data Structure



  startNetwork();
  startWebServer();
  startNTPClient();

  // initialisiert OTA
  ArduinoOTA.setHostname("AirSens");
  ArduinoOTA.setPassword("passwort");
  ArduinoOTA.begin();

  
}

void loop()
{
  ArduinoOTA.handle();
  
  delay(60000);
}

void LoopCore0(void *pvParameters)
{
  
  String timestamp;

  

  startVOCSensor(); //initialize the VOC Sensor

  for (;;)
  {
    timestamp = stringLocalTimestamp();


    loopVOCSensor();
    sendData(timestamp);
    delay(5000);
  }
}