cmake_minimum_required(VERSION 3.27)

project(VisionBridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(PYBIND11_FINDPYTHON ON)

find_package(Python 3.13 REQUIRED
    COMPONENTS Interpreter Development.Module
)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_visionbridge
    native/bindings.cpp
)

set_target_properties(_visionbridge PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY
        "$<1:${CMAKE_SOURCE_DIR}/visionbridge>"
    RUNTIME_OUTPUT_DIRECTORY
        "$<1:${CMAKE_SOURCE_DIR}/visionbridge>"
)

if(MSVC)
    target_compile_options(_visionbridge PRIVATE /W4 /permissive-)
endif()