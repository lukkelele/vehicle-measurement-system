#Description: IOCON Driver; user_visible: True
include_guard(GLOBAL)
message("driver_lpc_iocon_lite component is included.")

target_sources(${MCUX_SDK_PROJECT_NAME} PRIVATE
)

target_include_directories(${MCUX_SDK_PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}/.
)


include(driver_common)
