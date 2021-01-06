/**
 * WiFiManager advanced demo, contains advanced configurartion options
 * Implements TRIGGEN_PIN button press, press for ondemand configportal, hold for 3 seconds for reset settings.
 */

//--Libaries
#include <Arduino.h>
#include <WiFiManager.h> // https://github.com/tzapu/WiFiManager

//--Other-Files
#include <settings.h>
#include <file.h>

#define TRIGGER_PIN 0

//readConfig(); //Reads the config File

//--WiFi Manager OBJ
WiFiManager wm; // global wm instance

//WiFiManager extra Parameter
WiFiManagerParameter config_serveradress("serveradress", "Server", "", 40);
WiFiManagerParameter config_sensorid("sensorid", "Sensor-ID", "SENSOR_ID", 40); // global param ( for non blocking w params )
WiFiManagerParameter config_sensorsecret("sensorsecret", "Sensor-Secret", "SENSOR_SECRET", 40);

//--SPIFFS Config

//--Functions

void setup()
{

  loadSPIFFS(); //Initialize the Local Data Structure

  WiFi.mode(WIFI_STA); // explicitly set mode, esp defaults to STA+AP
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  delay(3000);
  Serial.println("\n Starting");

  pinMode(TRIGGER_PIN, INPUT);

  // add a custom input field
  wm.addParameter(&config_serveradress);
  wm.addParameter(&config_sensorid);
  wm.addParameter(&config_sensorsecret);

  // test custom html(radio)
  //const char* custom_radio_str = "<br/><label for='customfieldid'>Custom Field Label</label><input type='radio' name='customfieldid' value='1' checked> One<br><input type='radio' name='customfieldid' value='2'> Two<br><input type='radio' name='customfieldid' value='3'> Three";
  //new (&custom_field) WiFiManagerParameter(custom_radio_str); // custom html input

  // custom menu via array or vector
  //
  // menu tokens, "wifi","wifinoscan","info","param","close","sep","erase","restart","exit" (sep is seperator) (if param is in menu, params will not show up in wifi page!)
  // const char* menu[] = {"wifi","info","param","sep","restart","exit"};
  // wm.setMenu(menu,6);
  std::vector<const char *> menu = {"wifi", "info", "param", "sep", "restart", "exit"};
  wm.setMenu(menu);

  // set dark theme
  wm.setClass("invert");

  // wm.setConnectTimeout(20); // how long to try to connect for before continuing
  wm.setConfigPortalTimeout(120); // auto close configportal after n seconds
  wm.setAPClientCheck(true);      // avoid timeout if client connected to softap

  bool res;
  res = wm.autoConnect(APNAME, APPASSWORD); // Starts a password protectet AP

  if (!res)
  {
    Serial.println("Failed to connect or hit timeout");
    ESP.restart();
  }
  else
  {
    //if you get here you have connected to the WiFi
    Serial.println("-----------------------------");
    saveConfig(config_serveradress.getValue(), config_sensorid.getValue(), config_sensorsecret.getValue());
    readConfig();
    Serial.println("connected...yeey :)");
  }
}

void checkButton()
{
  // check for button press
  if (digitalRead(TRIGGER_PIN) == LOW)
  {
    // poor mans debounce/press-hold, code not ideal for production
    delay(50);
    if (digitalRead(TRIGGER_PIN) == LOW)
    {
      Serial.println("Button Pressed");
      // still holding button for 3000 ms, reset settings, code not ideaa for production
      delay(3000); // reset delay hold
      if (digitalRead(TRIGGER_PIN) == LOW)
      {
        Serial.println("Button Held");
        Serial.println("Erasing Config, restarting");
        wm.resetSettings();
        ESP.restart();
      }

      // start portal w delay
      Serial.println("Starting config portal");
      wm.setConfigPortalTimeout(120);

      if (!wm.startConfigPortal(APNAME, APPASSWORD))
      {
        Serial.println("failed to connect or hit timeout");
        delay(3000);
        // ESP.restart();
      }
      else
      {
        //if you get here you have connected to the WiFi
        Serial.println("-----------------------------");
        saveConfig(config_serveradress.getValue(), config_sensorid.getValue(), config_sensorsecret.getValue());
        readConfig();
        Serial.println("connected...yeey :)");
      }
    }
  }
}

String getParam(String name)
{
  //read parameter from server, for customhmtl input
  String value;
  if (wm.server->hasArg(name))
  {
    value = wm.server->arg(name);
  }
  return value;
}

void saveParamCallback()
{
  Serial.println("[CALLBACK] saveParamCallback fired");
  Serial.println("PARAM customfieldid = " + getParam("customfieldid"));
}

void loop()
{
  checkButton();
  // put your main code here, to run repeatedly:
}