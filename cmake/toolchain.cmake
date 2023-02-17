set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

#set(CMAKE_SYSROOT /usr/bin)
#set(CMAKE_STAGING_PREFIX /home/devel/stage)

set(tools /usr/bin)
#set(CMAKE_C_COMPILER "/usr/bin/gcc")
#set(CMAKE_C_COMPILER "/usr/bin/arm-none-eabi-gcc-12.2.0")
set(CMAKE_C_COMPILER "/home/lukas/Code/embedded/tools/arm-bcm2708/arm-linux-gnueabihf")
#set(CMAKE_CXX_COMPILER "/home/lukas/Code/embedded/tools/arm-bcm2708/arm-linux-gnueabihf")
#set(CMAKE_CXX_COMPILER ${tools}/arm-none-eabi-g++)
set(CMAKE_CXX_COMPILER "/usr/bin/g++")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
