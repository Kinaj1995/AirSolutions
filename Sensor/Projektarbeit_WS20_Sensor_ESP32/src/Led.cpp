

#include <Arduino.h>
#include <Led.h>

Led::Led(int red_pin, int green_pin, int blue_pin)
{
    pinMode(red_pin, OUTPUT);
    pinMode(green_pin, OUTPUT);
    pinMode(blue_pin, OUTPUT);

    _r = red_pin;
    _g = green_pin;
    _b = blue_pin;

    digitalWrite(_r, LOW);
    digitalWrite(_g, LOW);
    digitalWrite(_b, LOW);
}

void blink(int pin, int duration, int ammount)
{
    for (int i = 0; i < ammount; i++)
    {
        digitalWrite(pin, HIGH);
        delay(duration);
        digitalWrite(pin, LOW);
        delay(duration);
    }
}

void Led::shutoff_all()
{
    digitalWrite(_r, LOW);
    digitalWrite(_g, LOW);
    digitalWrite(_b, LOW);
}

void Led::startup(int blinkcount)
{
    for (int i = 0; i < 20; i++)
    {
        digitalWrite(_r, HIGH);
        digitalWrite(_g, HIGH);
        digitalWrite(_b, HIGH);
        delay(500);
        digitalWrite(_r, LOW);
        digitalWrite(_g, LOW);
        digitalWrite(_b, LOW);
        delay(500);
    }
}

void Led::displayval(int value)
{

    shutoff_all();

    switch (value)
    {
    case 0 ... 1500:
        digitalWrite(_g, HIGH);
        break;

    case 1501 ... 3000:
        digitalWrite(_b, HIGH);
        break;

    case 3001 ... 4000:
        digitalWrite(_r, HIGH);
        break;

    case 4001 ... 65000:
        blink(_r, 200, 20);
        break;

    default:
        break;
    }
}
