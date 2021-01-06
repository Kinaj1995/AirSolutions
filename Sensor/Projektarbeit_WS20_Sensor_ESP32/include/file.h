#include "FS.h"
#include "SPIFFS.h"


extern void loadSPIFFS();

extern void saveConfig(String server, String sensor_id, String sensor_secret);
extern void readConfig();