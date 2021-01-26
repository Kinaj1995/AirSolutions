#include "FS.h"
#include "SPIFFS.h"


extern void loadSPIFFS();
extern void saveData(String timestamp);
extern void writeFile(fs::FS &fs, const char *path, const char *message);
extern void deleteFile(const char *path);