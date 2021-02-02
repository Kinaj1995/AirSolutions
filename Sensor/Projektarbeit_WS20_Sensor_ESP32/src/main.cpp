//--Libaries
#include <Arduino.h>
#include <ArduinoOTA.h>

//--Other-Files
#include <settings.h>
#include <file.h>
#include <network.h>
#include <sensor.h>
#include <ntp.h>
#include <Led.h>

//--Init LED
Led led(led_red,led_green,led_blue); // Red, Green, Blue LED Pins

//--Loopcounter
int saveloop = 0;
int uploadloop = uploadDataInterval;

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

  startNetwork();   //Starts the WLAN Connection
  startWebServer(); //Starts the WebServer
  startNTPClient(); //Starts the NTP Client to sync Time

  // initialisiert OTA
  ArduinoOTA.setHostname(OTANAME);
  ArduinoOTA.setPassword(OTAPW);
  ArduinoOTA.begin();

  led.startup(10); // Startup with 10 Flashes



}

void loop()
{
  ArduinoOTA.handle(); //Handles over the air update
}

void LoopCore0(void *pvParameters)
{

  String timestamp;
  syncNTPClient(); // Syncs the internal RTC with the NTP Server

  startSensor(); //initialize the Sensors

  for (;;)
  {
    timestamp = stringLocalTimestamp(); // gets local time from RTC

    loopSensor(); // gets sensor values



    //--LED-Output

    led.displayval(air_eCO2);

    //--Serial-Output

    if (enableSerial)
    {
      Serial.println("-----Sensor-Data-----");
      Serial.println(timestamp);
      Serial.printf("Temp: %s °C \n", String(air_temp));
      Serial.printf("Hum; %d %% \n", air_hum);
      Serial.printf("eCO2: %d ppm \n", air_eCO2);
      Serial.printf("TVOC: %d \n", air_tvoc);
      Serial.printf("H2: %d \n", air_h2);
      Serial.printf("Ethanol: %d \n", air_e);
      Serial.println("---------------------");
    }

    //--Loop-Checker
    if (saveloop >= saveDataInterval)
    {
      saveData(timestamp);
      saveloop = 0;
    }

    if (uploadloop >= uploadDataInterval)
    {
      sendData();
      uploadloop = 0;
    }

    //--Loop-Land
    saveloop++;
    uploadloop++;

    delay(1000);
  }
}