#pragma once

#include <string>

#include "Log.h"
//#include "mosquitto.h"
#include <mosquitto.h>


class MQTTHandler
{
public:
    MQTTHandler(std::string& addr, uint16_t port);
    ~MQTTHandler() = default;

    void connect(std::string& addr = m_Address, uint16_t port = m_Port);

private:
    mosquitto* m_Client;
    bool m_InitializedMQQT = false;
    std::string m_Address = "localhost";
    uint16_t m_Port = 1883; 

};

