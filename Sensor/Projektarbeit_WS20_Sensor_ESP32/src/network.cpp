#include <Arduino.h>
#include <WiFi.h>
#include "ESPAsyncWebServer.h"
#include <ArduinoJson.h>
#include <HTTPClient.h>

#include <file.h>
#include <settings.h>
#include <network.h>
#include <ntp.h>

String processor(const String &var);

AsyncWebServer server(80); //Webserver Port

void startNetwork()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(SSID);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void startWebServer()
{

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/index.html", String(), false, processor);
  });

  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/style.css", "text/css");
  });

  server.on("/_js/diagramm.js", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/_js/diagramm.js", "text/javascript");
  });

  server.on("/sendata", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send_P(200, "text/plain", String(air_eCO2).c_str());
  });

  server.begin();
  Serial.println("HTTP server started");
}

String processor(const String &var)
{
  //Serial.println(var);

  if (var == "AIR_CO2")
  {
    return String(air_eCO2);
  }
  else if (var == "AIR_HUM")
  {
    return String(air_hum);
  }
  else if (var == "AIR_TEMP")
  {
    return String(air_temp);
  }
  else if (var == "SENSOR_ID")
  {
    return String(SENSOR_ID);
  }
    else if (var == "TIME")
  {
    return String(stringLocalTimestamp());
  }
  return String();
}

void sendData(String timestamp)
{
  if (WiFi.status() == WL_CONNECTED)
  {

    // Prepare JSON document
    DynamicJsonDocument doc(200);
    doc["sensor_id"] = SENSOR_ID;
    doc["sensor_secret"] = SENSOR_SECRET;
    doc["co2"] = air_eCO2;
    doc["temp"] = air_temp;
    doc["hum"] = air_hum;
    doc["timestamp"] = timestamp;

    String json;
    serializeJson(doc, json);

    Serial.println(json);

    HTTPClient http;

    
    http.begin("http://192.168.0.55:5000/sensors/api/savedata");
    http.addHeader("content-type", "application/json");
    int httpResponseCode = http.POST(json);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    http.end();
    
  }
  else
  {
    Serial.println("Not connected to WLAN!");
  }
}
