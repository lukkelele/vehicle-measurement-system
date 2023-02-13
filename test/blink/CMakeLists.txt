cmake_minimum_required(VERSION 3.12)

# Import based on PICO_SDK_PATH variable
include(pico_sdk_import.cmake)


project(test_Blink)

add_executable(blink blink/blink.cpp)
# Init Pico SDK
pico_sdk_init()
# pull in common dependencies
target_link_libraries(blink pico_stdlib freertos)

add_subdirectory(freertos)
#add_subdirectory(blink)

# add url via pico_set_program_url
# example_auto_set_url(blink)
