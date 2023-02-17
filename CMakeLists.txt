cmake_minimum_required(VERSION 3.12)

set(PROJECT_NAME VMS)
set(PROJECT_SRC_DIR VMS/src)
set(PROJECT_INCLUDE_DIR VMS/include)

#set(GCC_COVERAGE_COMPILE_FLAGS "-fprofile-arcs -ftest-coverage")
set(GCC_COVERAGE_COMPILE_FLAGS "-D_M_CEE")
add_definitions(${GCC_COVERAGE_COMPILE_FLAGS})
#-D_M_CEE

include(cmake/pico_sdk_import.cmake)
include(cmake/find_opencv.cmake)

project(${PROJECT_NAME} LANGUAGES C CXX ASM)
enable_language(C CXX ASM)

set(CMAKE_CXX_STANDARD 11)

find_package(OpenCV REQUIRED)
pico_sdk_init()


include_directories(
  ${PROJECT_INCLUDE_DIR}
  ${OpenCV_INCLUDE_DIRS}
)

add_executable(${PROJECT_NAME}
  ${PROJECT_SRC_DIR}/main.cpp 
  ${PROJECT_SRC_DIR}/VMS.cpp
  ${PROJECT_SRC_DIR}/Camera.cpp
)

target_link_libraries(${PROJECT_NAME} PUBLIC
  pico_stdlib
  hardware_uart
  hardware_gpio 
  freertos
  ${OpenCV_LIB_DIR}
)

add_subdirectory(lib/freertos)

pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 1)
pico_add_extra_outputs(VMS)
