cmake_minimum_required(VERSION 3.12)

set(OPENSSL_ROOT_DIR /usr/lib/openssl-1.1)
set(OPENSSL_INCLUDE_DIR /usr/include/openssl-1.1)

set(PROJECT_NAME VMS)
set(INCLUDE_DIR VMS/include)
set(SRC_DIR VMS/src)
set(VMS_LIBS lib)
set(PICO_EXTERNAL_LIB lib/pico-sdk/external)

include(${PICO_EXTERNAL_LIB}/pico_sdk_import.cmake)
include(cmake/find_mosquitto.cmake)

project(${PROJECT_NAME} VERSION 1.0 LANGUAGES C CXX ASM)

find_package(PkgConfig REQUIRED)
pkg_check_modules(Mosquitto IMPORTED_TARGET libmosquitto REQUIRED)

include_directories(
  ${INCLUDE_DIR}
  )

add_executable(VMS ${SRC_DIR}/main.cpp ${SRC_DIR}/VMS.cpp)

pico_sdk_init()

set_target_properties(${PROJECT_NAME} PROPERTIES VERSION ${PROJECT_VERSION})
target_link_libraries(
  VMS
  pico_stdlib
  hardware_uart
  hardware_gpio 
  freertos
  PkgConfig::Mosquitto
  )

add_subdirectory(lib/freertos)


pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
pico_add_extra_outputs(VMS)

include(GNUInstallDirs)
install(TARGETS ${PROJECT_NAME})
install(FILES mosquitto.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
