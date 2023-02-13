cmake_minimum_required(VERSION 3.12)

include(pico_sdk_import.cmake)


project(VehicleMeasurementSystem)
# enable_language( C CXX ASM )

add_executable(VMS src/VMS.cpp)

# include(lib/pico-sdk/external/pico_sdk_import.cmake)
pico_sdk_init()

# pull in common dependencies
target_link_libraries(VMS pico_stdlib hardware_uart hardware_gpio freertos)

add_subdirectory(lib/freertos)
#pico_enable_stdio_usb()
#pico_add_extra_outputs(VMS)
#add_subdirectory(pico-sdk)
