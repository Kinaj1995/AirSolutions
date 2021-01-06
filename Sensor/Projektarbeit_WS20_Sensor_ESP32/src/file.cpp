#include <FS.h>
#include <SPIFFS.h>
#include <ArduinoJson.h>

#include <Settings.h>

#define FORMAT_SPIFFS_IF_FAILED true

void loadSPIFFS()
{
    if (!SPIFFS.begin(FORMAT_SPIFFS_IF_FAILED))
    {
        Serial.println("SPIFFS Mount Failed");
        return;
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

void saveConfig(String server, String sensor_id, String sensor_secret)
{
    StaticJsonDocument<100> doc;
    doc = doc["system-config"];
    doc["system-config"]["server"] = server;
    doc["system-config"]["sensor_id"] = sensor_id;
    doc["system-config"]["sensor_secret"] = sensor_secret;

    File configFile = SPIFFS.open("/system_config.json", "r");
    if (!configFile)
    {
        Serial.println("Creating new file");
        writeFile(SPIFFS, "/system_config.json", "");
    }
    configFile = SPIFFS.open("/system_config.json", "w");
    serializeJsonPretty(doc, configFile);
    configFile.close();

    return;
}

void readConfig()
{
    File configfile = SPIFFS.open("/system_config.json", "r");
    StaticJsonDocument<100> doc;

    if (!configfile)
    {
        Serial.println("!No Data file Found! \n!Using basic settings!");
        return;
    }
    else
    {
        deserializeJson(doc, configfile);
        //serializeJsonPretty(doc, Serial);

        JsonObject obj = doc.as<JsonObject>();

        String server = obj["system-config"]["server"];
        String sensor_id = obj["system-config"]["sensor_id"];
        String sensor_secret = obj["system-config"]["sensor_secret"];

        SERVER = server;
        SENSOR_ID = sensor_id;
        SENSOR_SECRET = sensor_secret;

        Serial.println("--Datafile loaded--");

        return;
    }
}
