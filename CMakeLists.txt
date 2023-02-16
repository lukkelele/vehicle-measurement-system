cmake_minimum_required(VERSION 3.12)

set(OPENSSL_ROOT_DIR /usr/lib/openssl-1.1)
set(OPENSSL_INCLUDE_DIR /usr/include/openssl-1.1)

# Mosquitto
set(MOSQUITTO_INCLUDE_DIR lib/mosquitto/include)
set(MOSQUITTO_LIBRARY lib/mosquitto/lib)

set(PROJECT_NAME VMS)
set(INCLUDE_DIR VMS/include)
set(SRC_DIR VMS/src)
set(VMS_LIBS lib)
set(PICO_EXTERNAL_LIB lib/pico-sdk/external)

include(${PICO_EXTERNAL_LIB}/pico_sdk_import.cmake)

project(${PROJECT_NAME} VERSION 1.0 LANGUAGES C CXX ASM)

#add_subdirectory(lib/mosquitto)

include_directories(
  ${INCLUDE_DIR}
  lib/mosquitto/include
  lib/mosquitto/lib/include
  lib/mosquitto/lib
  /usr/include
  )

add_executable(VMS ${SRC_DIR}/main.cpp ${SRC_DIR}/VMS.cpp)

add_library(mosquitto lib/mosquitto/lib/mosquitto.c) 
install(TARGETS mosquitto)
install(FILES mosquitto.h DESTINATION ${PROJECT_NAME}/include)

#target_include_directories(${PROJECT_NAME} PUBLIC lib/mosquitto/lib)

pico_sdk_init()


target_link_libraries(
  VMS
  pico_stdlib
  hardware_uart
  hardware_gpio 
  freertos
  mosquitto
  )

add_subdirectory(lib/freertos)

pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
pico_add_extra_outputs(VMS)

#include(GNUInstallDirs)
#install(TARGETS ${PROJECT_NAME})
#install(FILES mosquitto.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
