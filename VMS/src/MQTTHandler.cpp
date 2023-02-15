#include "MQTTHandler.h"


MQTTHandler::MQTTHandler(std::string& addr, uint16_t port)
{
    m_Address = addr;
    m_Port = port;
    m_InitializedMQQT = mosquitto_lib_init();
}

void MQTTHandler::connect(std::string &addr, uint16_t port)
{
    if (m_InitializedMQQT)
    {
        m_Client = mosquitto_new("VMSystem-MQTT-Client", true, nullptr);
    } else {
        LOG("MQTT Client could NOT connect correctly!");
    }
}
