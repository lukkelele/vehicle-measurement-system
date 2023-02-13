cmake_minimum_required(VERSION 3.12)

project(VMS)
enable_language( C CXX ASM )

include(./lib/pico-sdk/external/pico_sdk_import.cmake)
pico_sdk_init()

add_executable( VMS src/VMS.cpp)

FILE(GLOB FreeRTOS_src lib/freertos/FreeRTOS-Kernel/*.c)

add_library(
  FreeRTOS STATIC ${FreeRTOS_src}
  lib/freertos/FreeRTOS-Kernel/portable/GCC/ARM_CM0/port.c
  lib/freertos/FreeRTOS-Kernel/portable/MemMang/heap_4.c
  )

target_include_directories (
  FreeRTOS PUBLIC lib/freertos/FreeRTOS-Kernel/include
  src/VMS.h
  src/VMSPico.h
  )

# pull in common dependencies
target_link_libraries(
  VMS
  pico-sdk/pico_stdlib
  hardware_uart
  hardware_gpio
  )

#pico_enable_stdio_usb()
#pico_add_extra_outputs(VMS)
