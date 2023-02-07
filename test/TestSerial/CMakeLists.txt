cmake_minimum_required(VERSION 3.12)

# Import based on PICO_SDK_PATH variable
include(pico_sdk_import.cmake)

include(example_auto_set_url.cmake)

project(test_Serial)
pico_sdk_init()

# Init Pico SDK

# pull in common dependencies
# target_link_libraries(serial pico_stdlib freertos)

# pico_add_extra_outputs(serial)


# add url via pico_set_program_url
# example_auto_set_url(serial)

add_subdirectory(freertos)
add_subdirectory(serial)
