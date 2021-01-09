#include <Arduino.h>

extern void startNTPClient();
extern void syncNTPClient();

extern String stringLocalTime();
extern String stringLocalDate();
extern String stringLocalTimestamp();