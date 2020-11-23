cmake_minimum_required(VERSION 3.6)
project(PackageTest Swift OBJC)

set(CONAN_DISABLE_CHECK_COMPILER ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(example
    AppDelegate.swift
)
target_link_libraries(example ${CONAN_LIBS})

set_target_properties(example
    PROPERTIES
    OUTPUT_NAME test
    MACOSX_BUNDLE_INFO_PLIST "${CMAKE_CURRENT_LIST_DIR}/plist.in"
)
