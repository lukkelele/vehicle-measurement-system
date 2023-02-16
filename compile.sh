#!/bin/bash

# This needs to be run at ROOT

./clean.sh
# cmake --debug-output -B ./build -S .
cmake -B ./build -S .
make -C build
