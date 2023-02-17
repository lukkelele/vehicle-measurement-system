#!/bin/bash

./clean.sh
# cmake --debug-output -B ./build -S .
#cmake -DCMAKE_BUILD_TYPE=Debug -B ./build -S .
cmake --debug-output -B ./build -S .
make -C build
