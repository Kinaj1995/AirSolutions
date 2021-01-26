#include <FS.h>
#include <SPIFFS.h>
#include <ArduinoJson.h>

#include <settings.h>
#include <file.h>

#define FORMAT_SPIFFS_IF_FAILED true

void loadSPIFFS()
{
    if (!SPIFFS.begin(FORMAT_SPIFFS_IF_FAILED))
    {
        Serial.println("SPIFFS Mount Failed");
        return;
    }
}

void deleteFile(const char *path)
{
    Serial.printf("Writing file: %s\r\n", path);

    File delFile = SPIFFS.open("/system_config.json", "r");

    if (!delFile)
    {
        Serial.println("File does not exists.");
    }
    else
    {
        SPIFFS.remove(path);
        Serial.println("File got deleted.");
    }
}

void writeFile(fs::FS &fs, const char *path, const char *message)
{
    Serial.printf("Writing file: %s\r\n", path);

    File file = fs.open(path, FILE_WRITE);
    if (!file)
    {
        Serial.println("- failed to open file for writing");
        return;
    }
    if (file.print(message))
    {
        Serial.println("- file written");
    }
    else
    {
        Serial.println("- write failed");
    }
    file.close();
}

void saveData(String timestamp)
{

    File dataFile = SPIFFS.open("/sendata.json", "r");
    StaticJsonDocument<2048> doc;

    try
    {
        deserializeJson(doc, dataFile);
        doc["sensor_id"] = SENSOR_ID;
        doc["sensor_secret"] = SENSOR_SECRET;

        JsonObject data = doc["data"].createNestedObject();

        data["co2"] = air_eCO2;
        data["temp"] = air_temp;
        data["hum"] = air_hum;
        data["timestamp"] = timestamp;
        data["tvoc"] = air_tvoc;
        data["h2"] = air_h2;
        data["ethanol"] = air_e;

        dataFile = SPIFFS.open("/sendata.json", "w");
        serializeJsonPretty(doc, dataFile);

        dataFile.close();
        Serial.println("Data got stored");
    }
    catch (const std::exception &e)
    {
        Serial.println("Creating JSON File");

        deleteFile("/sendata.json");
        
        deserializeJson(doc, dataFile);
        doc["sensor_id"] = SENSOR_ID;
        doc["sensor_secret"] = SENSOR_SECRET;

        JsonObject data = doc["data"].createNestedObject();

        data["co2"] = air_eCO2;
        data["temp"] = air_temp;
        data["hum"] = air_hum;
        data["timestamp"] = timestamp;
        data["tvoc"] = air_tvoc;
        data["h2"] = air_h2;
        data["ethanol"] = air_e;

        dataFile = SPIFFS.open("/sendata.json", "w");
        serializeJsonPretty(doc, dataFile);

        dataFile.close();
    }
}
