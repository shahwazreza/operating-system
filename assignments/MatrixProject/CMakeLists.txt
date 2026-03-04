cmake_minimum_required(VERSION 3.10)
project(MatrixProject LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Option to choose shared vs static build for the math library
option(BUILD_SHARED "Build MatrixMath as a shared library (DLL/.so)" ON)

if(BUILD_SHARED)
    add_library(MatrixMath SHARED matrix_math.cpp)
    # Define the macro so the header knows to EXPORT the symbols
    target_compile_definitions(MatrixMath PRIVATE BUILD_MATH_DLL)
else()
    add_library(MatrixMath STATIC matrix_math.cpp)
endif()

# Main executable
add_executable(MatrixApp main.cpp)

target_link_libraries(MatrixApp PRIVATE MatrixMath)

# Profiling executable (separate from MatrixApp to keep the original main clean)
add_executable(MatrixProfile profile_main.cpp)

target_link_libraries(MatrixProfile PRIVATE MatrixMath)

# Link extra lib on Windows for memory query APIs
if(WIN32)
    target_link_libraries(MatrixProfile PRIVATE Psapi)
endif()

# Place all outputs (exe, dll/so, lib) into a common folder for easier running
foreach(tgt IN ITEMS MatrixApp MatrixProfile MatrixMath)
    if(TARGET ${tgt})
        set_target_properties(${tgt} PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/$<CONFIG>
            ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/$<CONFIG>
            LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/$<CONFIG>
        )
    endif()
endforeach()

# Helpful warnings in debug builds
if(MSVC)
    target_compile_options(MatrixMath PRIVATE /W4)
    target_compile_options(MatrixApp PRIVATE /W4)
    target_compile_options(MatrixProfile PRIVATE /W4)
else()
    target_compile_options(MatrixMath PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(MatrixApp PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(MatrixProfile PRIVATE -Wall -Wextra -Wpedantic)
endif()
