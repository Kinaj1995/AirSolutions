/*
    led.h - To controll the Sensors LED to alert People
    


*/

#ifndef Led_h
#define Led_h

#include <Arduino.h>



class Led
{
private:
    int _r;
    int _g;
    int _b;

public:
    Led(int red_pin, int green_pin, int blue_pin);
    
    void startup(int blinkcount);
    void displayval(int value);
    void shutoff_all();
};


#endif
