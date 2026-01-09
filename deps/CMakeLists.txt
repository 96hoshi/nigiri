cmake_minimum_required(VERSION 3.10)
project(deps)

# Build order matters - dependencies must be built before dependents

# Resource embedding tool (needed by date and others)
add_subdirectory(res EXCLUDE_FROM_ALL)

# Testing libraries (needed by opentelemetry-cpp)
add_subdirectory(googletest EXCLUDE_FROM_ALL)
add_subdirectory(doctest EXCLUDE_FROM_ALL)

# protobuf (needed for gtfsrt)
add_subdirectory(abseil-cpp EXCLUDE_FROM_ALL)
add_subdirectory(protobuf EXCLUDE_FROM_ALL)

# Basic dependencies
add_subdirectory(cista EXCLUDE_FROM_ALL)
add_subdirectory(utl EXCLUDE_FROM_ALL)
add_subdirectory(fmt EXCLUDE_FROM_ALL)
add_subdirectory(date EXCLUDE_FROM_ALL)
add_subdirectory(miniz EXCLUDE_FROM_ALL)
add_subdirectory(wyhash EXCLUDE_FROM_ALL)
add_subdirectory(unordered_dense EXCLUDE_FROM_ALL)
add_subdirectory(oh EXCLUDE_FROM_ALL)
add_subdirectory(pugixml EXCLUDE_FROM_ALL)
add_subdirectory(json EXCLUDE_FROM_ALL)

# zlib (needed for boost and others)
add_subdirectory(zlib-ng EXCLUDE_FROM_ALL)

# boost
add_subdirectory(boost EXCLUDE_FROM_ALL)

# opentelemetry (requires protobuf and googletest)
add_subdirectory(opentelemetry-proto EXCLUDE_FROM_ALL)
add_subdirectory(opentelemetry-cpp EXCLUDE_FROM_ALL)

# PROJ dependencies
add_subdirectory(libressl EXCLUDE_FROM_ALL)
add_subdirectory(curl EXCLUDE_FROM_ALL)
add_subdirectory(sqlite3 EXCLUDE_FROM_ALL)
add_subdirectory(tg EXCLUDE_FROM_ALL)
add_subdirectory(PROJ EXCLUDE_FROM_ALL)

# Geo
add_subdirectory(rtree.c EXCLUDE_FROM_ALL)
add_subdirectory(geo EXCLUDE_FROM_ALL)

# Lua
add_subdirectory(LuaJIT EXCLUDE_FROM_ALL)
add_subdirectory(sol2 EXCLUDE_FROM_ALL)

# PEGTL parser
add_subdirectory(PEGTL EXCLUDE_FROM_ALL)

# Documentation
add_subdirectory(docs EXCLUDE_FROM_ALL)
