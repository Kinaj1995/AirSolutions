#include <Wire.h>
#include <Adafruit_SGP30.h>
#include <Adafruit_AM2320.h>

#include <settings.h>

//--init VOC Sensor
unsigned int eco2;
unsigned int tvoc;
int hum;
float temp;

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

    
}



void loopSensor()
{

    while (!sgp.IAQmeasure())
    {
        Serial.print(".");
        delay(100);
    }

    air_eCO2 = ((19 * air_eCO2) + sgp.eCO2) / 20;
    air_tvoc = ((19 * air_tvoc) + sgp.TVOC) / 20;
    air_h2 = sgp.rawH2;
    air_e = sgp.rawEthanol;    

    air_temp = ((19 * air_temp) + am2320.readTemperature()) / 20;
    air_hum = ((19 * air_hum ) + am2320.readHumidity()) / 20;


}




