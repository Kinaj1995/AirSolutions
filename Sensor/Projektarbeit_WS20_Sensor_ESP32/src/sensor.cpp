#include <Wire.h>
#include <Adafruit_SGP30.h>

#include <settings.h>

//--init VOC Sensor
unsigned int eco2;
unsigned int tvoc;

unsigned long entryLoop, entryPublish;

Adafruit_SGP30 sgp;



void startVOCSensor()
{
    if (!sgp.begin())
    {
        Serial.println("Sensor not found :(");
        while (1);
    }
    else
    {
        sgp.setHumidity(8200); //8200 mg/m3 humidity (35% at 25 degrees)
    }

    Serial.println("Calibrating Sensort:");
    do
    {
        while (!sgp.IAQmeasure())
        {
            Serial.print(".");
            delay(100);
        }
        Serial.print(".");
        eco2 = sgp.eCO2;
        
    } while (eco2 == 400);
    entryLoop = millis();
}

void loopVOCSensor()
{
    
    while (!sgp.IAQmeasure())
    {
        Serial.print(".");
        delay(100);
    }

    tvoc = ((19 * tvoc) + sgp.TVOC) / 20;
    Serial.print("TVOC(ppb):");
    Serial.print(tvoc);

    eco2 = ((19 * eco2) + sgp.eCO2) / 20;
    Serial.print(" eco2(ppm):");
    Serial.println(eco2);

    air_eCO2 = eco2;


    
}