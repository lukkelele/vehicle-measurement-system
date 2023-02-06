cmake_minimum_required(VERSION 3.12)

find_package(Perl)
if(NOT PERL_FOUND)
    message(FATAL_ERROR "Perl is needed for generating the fsdata.c file")
endif()

include(cmake/utils.cmake) # Holds function to suppress tinyusb warnings
include(lib/pico-sdk/external/pico_sdk_import.cmake)


if(EXISTS cmake/credentials.cmake)
    # copy it over from cmake/credentials.cmake.example
    include(cmake/credentials.cmake)
else()
    message(WARNING "Credentials file not found, using default values!")
    set(WIFI_SSID "SSID" CACHE INTERNAL "[INSERT DEFAULT]")
    set(WIFI_PASSWORD "password" CACHE INTERNAL "[INSERT DEFAULT]")
endif()

set(PICO_BOARD pico_w)

project(VehicleMeasurementSystem C CXX ASM)
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

add_compile_options(
        -Wall
        -Werror
)

# Init Pico SDK
pico_sdk_init()

# pull in common dependencies
# target_link_libraries(src pico_stdlib)

add_subdirectory(src)
