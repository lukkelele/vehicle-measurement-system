project "Mosquitto"
    kind "StaticLib"
    language "C"
    staticruntime "on"

    targetdir "build/" .. outputdir .. "%{prj.name}"
    objdir "build/obj/" .. outputdir .. "%{prj.name}"

    includedirs
    { 
     -- "mosquitto-2.0.13/lib"
      "lib",
      "include"
    }

    links
    {
      "mosquitto"
    }

    files { "src/**.c" }

    filter "configurations:Debug"
        defines { "DEBUG" }
        symbols "on"

    filter "configurations:Release"
        defines { "RELEASE" }
        optimize "on"

    filter "platforms:x64"
        architecture "x86_64"
