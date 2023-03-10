#include <Arduino.h>

//Sensor Information
extern String SERVER;
extern String SERVERPORT;
extern String SENSOR_ID;
extern String SENSOR_SECRET;
extern const int saveDataInterval;
extern const int uploadDataInterval;

//Wifi 
extern const char* SSID;
extern const char* PASSWORD;

// OTA Update
extern const char* OTANAME;
extern const char* OTAPW;

// NTP
extern const char *ntpServer;
extern const long gmtOffset_sec;
extern const int daylightOffset_sec;
extern const int ntpSyncInterval;

// Serial Output
extern boolean enableSerial;

//LED Pins
extern const int led_green;
extern const int led_blue;
extern const int led_red;

//Global Vars
extern int air_eCO2;
extern int air_tvoc;
extern int air_hum;
extern int air_h2;
extern int air_e;
extern float air_temp;