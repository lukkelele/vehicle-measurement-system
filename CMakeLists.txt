cmake_minimum_required(VERSION 3.12)

set(PROJECT_NAME VMS)
set(PROJECT_SRC_DIR VMS/src)
set(PROJECT_INCLUDE_DIR VMS/include)

include(FindPkgConfig)
find_package(PkgConfig REQUIRED)
pkg_check_modules(Mosquitto IMPORTED_TARGET libmosquitto REQUIRED)

include(lib/pico_sdk_import.cmake)
project(${PROJECT_NAME} VERSION 1.0 LANGUAGES C CXX ASM)
pico_sdk_init()

#add_library(mosquitto SHARED IMPORTED GLOBAL)
#find_package(mosquitto REQUIRED)
#set_target_properties(mosquitto PROPERTIES IMPORTED_LOCATION /usr/local/lib/libmosquitto.so.1)
#set_target_properties(mosquitto PROPERTIES IMPORTED_LOCATION /usr/lib/libmosquitto.so.1)
#set_target_properties(mosquitto PROPERTIES IMPORTED_LOCATION lib/mosquitto/lib/libmosquitto.so.1)
add_executable(${PROJECT_NAME}
  ${PROJECT_SRC_DIR}/main.cpp 
  ${PROJECT_SRC_DIR}/VMS.cpp
)

set_target_properties(${PROJECT_NAME} PROPERTIES VERSION ${PROJECT_VERSION})

include_directories(
  ${PROJECT_INCLUDE_DIR}
)

target_link_libraries(${PROJECT_NAME} PUBLIC
  pico_stdlib
  hardware_uart
  hardware_gpio 
  freertos
  #mosquitto
  PkgConfig::Mosquitto
)

add_subdirectory(lib/freertos)

pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
pico_add_extra_outputs(VMS)

include(GNUInstallDirs)
install(TARGETS ${PROJECT_NAME})
install(FILES ${PROJECT_INCLUDE_DIR}/VMS.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
