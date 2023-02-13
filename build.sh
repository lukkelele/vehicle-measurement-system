#!/bin/bash


cd ./build
# cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug ../src
cmake --build .. --target VMS
