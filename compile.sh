#!/bin/bash

# This needs to be run at ROOT

cmake -B ./build -S .
make -C build
