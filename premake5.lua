workspace "VehicleMeasurementSystem"
  configurations { "Debug", "Release" }
  architecture "arm"
  system "raspberrypi"

project "VehicleMeasurementSystem"
  kind "ConsoleApp"
  language "C++"
  cppdialect "C++17"
  targetdir "bin/%{cfg.buildcfg}"

  files {
    "src/**.h",
    "src/**.cpp"
  }

  filter "configurations:Debug"
    defines { "DEBUG" }
    symbols "On"

  filter "configurations:Release"
    defines { "NDEBUG" }
    optimize "On"

toolchain "gcc"
