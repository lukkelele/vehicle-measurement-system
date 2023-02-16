cmake_minimum_required(VERSION 3.12)

set(PROJECT_NAME VMS)
set(INCLUDE_DIR VMS/include)
set(SRC_DIR VMS/src)
set(CMAKE_SCRIPT_DIR cmake)
set(PICO_EXTERNAL_LIB lib/pico-sdk/external)

include(${PICO_EXTERNAL_LIB}/pico_sdk_import.cmake)
include(${CMAKE_SCRIPT_DIR}/find_mosquitto.cmake)

project(${PROJECT_NAME} VERSION 1.0)
enable_language( C CXX ASM )

find_package(PkgConfig REQUIRED)
pkg_check_modules(Mosquitto IMPORTED_TARGET libmosquitto REQUIRED)

#add_executable(${PROJECT_NAME} MosquittoTest.cpp MosquittoInterface.h)



include_directories(${INCLUDE_DIR})

set(HEADER_FILES ${INCLUDE_DIR}/VMS.h)
set(SOURCES 
  ${SRC_DIR}/VMS.cpp 
  #${SRC_DIR}/MQTTHandler.cpp

  ${INCLUDE_DIR}/VMS.h
  #${INCLUDE_DIR}/MQTTHandler.h
  #${INCLUDE_DIR}/Log.h
  )

# add_executable(VMS ${SRC_DIR}/main.cpp ${SOURCES})
add_executable(VMS ${SRC_DIR}/main.cpp ${SRC_DIR}/VMS.cpp)

set_target_properties(${PROJECT_NAME} PROPERTIES VERSION ${PROJECT_VERSION})

pico_sdk_init()

target_link_libraries(
  VMS
  pico_stdlib
  hardware_uart
  hardware_gpio 
  freertos
  PkgConfig::Mosquitto
  )

add_subdirectory(lib/freertos)

include(GNUInstallDirs)
install(TARGETS ${PROJECT_NAME})
install(FILES MosquittoInterface.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
pico_add_extra_outputs(VMS)
