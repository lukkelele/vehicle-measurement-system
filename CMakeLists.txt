cmake_minimum_required(VERSION 3.12)

set(PROJECT_NAME VMS)
set(PICO_EXTERNAL_LIB lib/pico-sdk/external)
include(${PICO_EXTERNAL_LIB}/pico_sdk_import.cmake)


project(${PROJECT_NAME})
enable_language( C CXX ASM )


add_executable(VMS src/VMS.cpp)

pico_sdk_init()

target_link_libraries(VMS pico_stdlib hardware_uart hardware_gpio freertos)
add_subdirectory(lib/freertos)

pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
pico_add_extra_outputs(VMS)

