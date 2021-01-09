#include <Arduino.h>

//Sensor Information
extern String SERVER;
extern String SERVERPORT;
extern String SENSOR_ID;
extern String SENSOR_SECRET;

//Wifi 
extern const char* SSID;
extern const char* PASSWORD;

// NTP
extern const char *ntpServer;
extern const long gmtOffset_sec;
extern const int daylightOffset_sec;
extern const int ntpSyncInterval;


//Global Vars
extern int air_eCO2;
extern int air_hum;
extern float air_temp;