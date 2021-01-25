#include <Wire.h>
#include <Adafruit_SGP30.h>
#include <Adafruit_AM2320.h>

#include <settings.h>

//--init VOC Sensor
unsigned int eco2;
unsigned int tvoc;

Adafruit_SGP30 sgp;
Adafruit_AM2320 am2320 = Adafruit_AM2320();

void startSensor()
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

    am2320.begin(); //Startet den AM2320 Sensor

    for (int i = 0; i < 40; i++)
    {
        Serial.println(am2320.readTemperature());
    }
    
}



void loopSensor()
{

    while (!sgp.IAQmeasure())
    {
        Serial.print(".");
        delay(100);
    }

    tvoc = ((19 * tvoc) + sgp.TVOC) / 20;
    eco2 = ((19 * eco2) + sgp.eCO2) / 20;

    air_eCO2 = eco2;
    air_tvoc = tvoc;

    while (!sgp.IAQmeasureRaw())
    {
        Serial.print(".");
        delay(100);
    }
    air_h2 = sgp.rawH2;
    air_e = sgp.rawEthanol;


    air_temp = am2320.readTemperature();
    air_hum = am2320.readHumidity();


}