cmake_minimum_required(VERSION 3.12)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_PREFIX_PATH "/usr/local/lib")

#include(FetchContent)
#include(cmake/build_info.cmake)
#set(CMAKE_TOOLCHAIN_FILE cmake/toolchain.cmake)
#include(cmake/find_opencv.cmake)
include(cmake/pico_sdk_import.cmake)

set(PROJECT_NAME VMS)
set(PROJECT_SRC_DIR ${PROJECT_NAME})
set(PROJECT_INCLUDE_DIR ${PROJECT_NAME})
set(OpenCV_DIR "lib/opencv/build/lib")

project(${PROJECT_NAME} LANGUAGES C CXX ASM)
pico_sdk_init()
#find_package(OpenCV REQUIRED)
find_package(raspicam REQUIRED)

add_compile_options(-Wall -Wno-format -Wno-unused-function -Wno-maybe-uninitialized -Wno-unused-variable)

message("C COMPILER: " ${CMAKE_C_COMPILER})
message("CXX COMPILER: " ${CMAKE_CXX_COMPILER})

include_directories( ${PROJECT_INCLUDE_DIR} )

add_executable(${PROJECT_NAME}
  ${PROJECT_NAME}/main.cpp
)

#FetchContent_Declare(
#  freertos_kernel
#  GIT_REPOSITORY https://github.com/FreeRTOS/FreeRTOS-Kernel.git
#  GIT_TAG        main #Note: Best practice to use specific git-hash or tagged version
#)

target_link_libraries(${PROJECT_NAME} PUBLIC
  #pico_stdlib
  #hardware_uart
  #hardware_gpio 
  #freertos
  ${raspicam_LIBS}
  #{OpenCV_LIBS}
)

add_subdirectory(lib/freertos)

pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
pico_add_extra_outputs(${PROJECT_NAME})
