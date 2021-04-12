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


//starts the webserver
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

//handels webserver request
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

  server.on("/sendata.json", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SPIFFS, "/sendata.json", "text/json");
  });

  server.begin();
  Serial.println("HTTP server started");
}


//Replaces Var in HTML file with sensor values
String processor(const String &var)
{
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

//sends the json file to the server
void sendData()
{
  if (WiFi.status() == WL_CONNECTED)
  {
    File dataFile = SPIFFS.open("/sendata.json", "r");
    DynamicJsonDocument doc(4096);

    if (!dataFile)
    {
      Serial.println("No file found");
      return;
    }
    else
    {
      deserializeJson(doc, dataFile);

      String json;
      serializeJson(doc, json);

      HTTPClient http;

      http.begin("https://as.puchtuning.synology.me/sensors/api/savedata");
      http.addHeader("content-type", "application/json");
      int httpResponseCode = http.POST(json);

      http.end();

      if(httpResponseCode == 200){
        Serial.println("Daten wurden vom Server gespeichert.");
        deleteFile("/sendata.json");

      } else{
        Serial.println("Daten konnten nicht gesopeichert werden.");
      }

      return;
    }

    
  }else{
    Serial.println("No Internet");
  }

}
