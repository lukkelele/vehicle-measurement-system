workspace "VehicleMeasurementSystem"
  configurations { "Debug" }
  
  filter "configurations:Debug"
    symbols "On"


project "VehicleMeasurementSystem"
  -- kind ""
  language "C++"
  cppdialect "C++17"
  
  targetdir "build/"

  includedirs {
    "include/"
  }

  files {
    "src/**.cpp",
    "src/**.h",
  }
