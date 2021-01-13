
#include <Arduino.h>
#include <settings.h>

//Sensor Information
String SERVER = "http://192.168.0.91:5000/sensors/api/savedata";
String SERVERPORT = "5000";
String SENSOR_ID = "PARU_HOME";
String SENSOR_SECRET = "PW12345w!";

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



//Global Vars
int air_eCO2;
int air_hum;
float air_temp;
