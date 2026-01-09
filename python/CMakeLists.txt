cmake_minimum_required(VERSION 3.22)
project(nigiri_python)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Disable -Werror
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-error -Wno-error=pessimizing-move")

# Find Python
find_package(Python REQUIRED COMPONENTS Interpreter Development)

# Find pybind11
execute_process(
    COMMAND ${Python_EXECUTABLE} -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
find_package(pybind11 CONFIG REQUIRED)

# Use existing nigiri build
set(NIGIRI_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/..)
include_directories(${NIGIRI_ROOT}/include)
include_directories(${NIGIRI_ROOT}/build/generated)
include_directories(${NIGIRI_ROOT}/deps/cista/include)
include_directories(${NIGIRI_ROOT}/deps/date/include)
include_directories(${NIGIRI_ROOT}/deps/fmt/include)
include_directories(${NIGIRI_ROOT}/deps/geo/include)
include_directories(${NIGIRI_ROOT}/deps/utl/include)
include_directories(${NIGIRI_ROOT}/deps/miniz)
include_directories(${NIGIRI_ROOT}/deps/pugixml/src)
include_directories(${NIGIRI_ROOT}/deps/unordered_dense/include)
include_directories(${NIGIRI_ROOT}/deps/wyhash)
include_directories(${NIGIRI_ROOT}/deps/PROJ/include)
include_directories(${NIGIRI_ROOT}/deps/protobuf/src)
include_directories(${NIGIRI_ROOT}/deps/oh/include)
include_directories(${NIGIRI_ROOT}/deps/opentelemetry-cpp/api/include)
include_directories(${NIGIRI_ROOT}/deps/opentelemetry-cpp/sdk/include)
include_directories(${NIGIRI_ROOT}/deps/abseil-cpp)

# Link to the built library
link_directories(${NIGIRI_ROOT}/build)
link_directories(${NIGIRI_ROOT}/build/deps/cista)
link_directories(${NIGIRI_ROOT}/build/deps/date)
link_directories(${NIGIRI_ROOT}/build/deps/fmt)
link_directories(${NIGIRI_ROOT}/build/deps/geo)
link_directories(${NIGIRI_ROOT}/build/deps/utl)
link_directories(${NIGIRI_ROOT}/build/deps/miniz)
link_directories(${NIGIRI_ROOT}/build/deps/pugixml)
link_directories(${NIGIRI_ROOT}/build/deps/unordered_dense)
link_directories(${NIGIRI_ROOT}/build/deps/wyhash)
link_directories(${NIGIRI_ROOT}/build/deps/PROJ/src)
link_directories(${NIGIRI_ROOT}/build/deps/protobuf)

# Create Python module
pybind11_add_module(_nigiri ${CMAKE_CURRENT_SOURCE_DIR}/bindings.cpp)

# Link all required libraries
target_link_libraries(_nigiri PRIVATE 
    nigiri
    gtfsrt
    protobuf
    proj
    date-tz
    fmt
)
