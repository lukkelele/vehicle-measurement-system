#!/bin/bash

# This needs to be run at ROOT

./clean.sh
cmake -B ./build -S .
make -C build
