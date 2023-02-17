#!/bin/bash

# This needs to be run at ROOT

./clean.sh
# cmake --debug-output -B ./build -S .
cmake -DCMAKE_BUILD_TYPE=Debug -B ./build -S .
make -C build
