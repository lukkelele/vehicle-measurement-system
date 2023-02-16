project "pico-SDK"
    kind "StaticLib"
    language "C"
    staticruntime "on"

    targetdir "bin/%{cfg.buildcfg}"
    includedirs { "/path/to/pico-sdk/headers" }

    libdirs { "/path/to/pico-sdk/build" }

    links 
    { 
      "pico_stdlib" 
    }

    files
    {
      "src/**.c"
    }

    filter "configurations:Debug"
        defines { "DEBUG" }
        symbols "on"

    filter "configurations:Release"
        defines { "RELEASE" }
        optimize "on"

    filter "platforms:arm"
        architecture "arm"
        toolset "gcc"
        buildoptions {
            "-mthumb",
            "-mcpu=cortex-m0",
            "-march=armv6-m",
            "-mfpu=vfp",
            "-mfloat-abi=hard"
        }
        linkoptions {
            "-nostartfiles",
            "-T/path/to/pico-sdk/src/rp2_common/cmsis/gcc_startup_nano.S",
            "-T/path/to/pico-sdk/src/rp2_common/cms
