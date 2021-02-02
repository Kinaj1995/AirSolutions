
#include <Arduino.h>
#include <settings.h>

//Sensor Information
String SERVER = "https://as.puchtuning.synology.me/sensors/api/savedata";
String SERVERPORT = "5000";
String SENSOR_ID = "PARU_HOME";
String SENSOR_SECRET = "PW12345w!";
const int saveDataInterval = 30;
const int uploadDataInterval =  300;

//Wifi
const char* SSID = "NoFreeWiFi";
const char* PASSWORD = "Fabc471608!";

// OTA Update
const char* OTANAME = "PARU_HOME";
const char* OTAPW = "12345";



// NTP Config
const char *ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 3600;
const int daylightOffset_sec = 3600;
const int ntpSyncInterval = 17280; //Once a Day (Default: 17'280)

// Serial Output
boolean enableSerial = false;

//LED Pins
const int led_green = 15;
const int led_blue = 2;
const int led_red = 4;

//Global Vars
int air_eCO2;
int air_tvoc;
int air_hum;
int air_h2;
int air_e;
float air_temp;
