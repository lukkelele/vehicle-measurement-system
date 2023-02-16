workspace "VehicleMeasurementSystem"
    configurations { "Debug", "Release" }
    platforms
    {
      "native", 
      "arm"
    }

    outputdir = "%{cfg.buildcfg}-%{cfg.system}"

include "lib/pico-sdk/premake5.lua"

project "VehicleMeasurementSystem"
    location "VMS"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    -- staticruntime "off"

    targetdir ("%{wks.location}/bin/" .. outputdir .. "/%{prj.name}")
    objdir ("%{wks.location}/bin-int/" .. outputdir .. "/%{prj.name}")

    files
    {
      "${prj.name}/**.h",
      "${prj.name}/**.cpp",
      "${prj.name}/**.c",
      "${prj.name}/**.hpp"
    }

    libdirs
    {
        "%{wks.location}/lib/mosquitto/lib",
        "%{wks.location}/lib/glfw/lib"
    }

    includedirs
    {
       "%{prj.name}/src",
       "%{wks.location}/lib",
       "%{wks.location}/lib/freertos",
       "%{wks.location}/lib/mosquitto",
       "%{wks.location}/lib/pico-sdk"
    }

    links
    {
      "pico-SDK"
    }
  

