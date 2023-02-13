cmake_minimum_required(VERSION 3.12)

project(VehicleMeasurementSystem C CXX ASM)

include(lib/pico-sdk/external/pico_sdk_import.cmake)

set(SOURCE_DIR ./src)
# project(VehicleMeasurementSystem C CXX ASM)

add_executable(
  VMS
  ${SOURCE_DIR}/VMS.cpp
  )

# Init Pico SDK
pico_sdk_init()

# pull in common dependencies
target_link_libraries(
  VMS
  pico_stdlib
  freertos
  src
  )

# add_subdirectory(src)
