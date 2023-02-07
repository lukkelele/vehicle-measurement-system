add_executable(
  serial
  serial.c
)

target_link_libraries(serial pico_stdlib freertos)
pico_add_extra_outputs(serial)
