#include <Arduino.h>
#include <time.h>

#include <ntp.h>
#include <settings.h>

int ntpsynccount = 0;

void startNTPClient()
{
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void syncNTPClient()
{
    //Sync Time
    if (ntpsynccount >= ntpSyncInterval)
    {
        configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
        ntpsynccount = 0;
    }

    // Loopcounter
    ntpsynccount++;

}

String stringLocalTime()
{
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo))
    {
        Serial.println("Failed to obtain time");
        return "Faild to load Time";
    }
    char timeStringBuff[50]; //50 chars should be enough
    strftime(timeStringBuff, sizeof(timeStringBuff), "%H:%M", &timeinfo);

    //Serial.println(timeStringBuff);

    return timeStringBuff;
}

String stringLocalDate()
{
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo))
    {
        Serial.println("Failed to obtain time");
        return "Faild to load Time";
    }
    char timeStringBuff[50]; //50 chars should be enough
    strftime(timeStringBuff, sizeof(timeStringBuff), "%d.%m.%Y", &timeinfo);

    //Serial.println(timeStringBuff);

    return timeStringBuff;
}

String stringLocalTimestamp()
{
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo))
    {
        Serial.println("Failed to obtain time");
        return "Faild to load Time";
    }
    char timeStringBuff[50]; //50 chars should be enough
    strftime(timeStringBuff, sizeof(timeStringBuff), "%d.%m.%Y %H:%M:%S", &timeinfo);

    //Serial.println(timeStringBuff);

    return timeStringBuff;
}
