cmake_minimum_required(VERSION 3.10)
project(MatrixProject)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1. Compile the Shared Library (DLL)
# "SHARED" tells CMake to make a .dll on Windows or .so on Linux
add_library(MatrixMath SHARED matrix_math.cpp)

# Define the macro so the header knows to EXPORT the functions
target_compile_definitions(MatrixMath PRIVATE BUILD_MATH_DLL)

# 2. Compile the Main Executable
add_executable(MatrixApp main.cpp)

# 3. Link the Library to the Executable
# This automatically handles linking the .lib import file on Windows
target_link_libraries(MatrixApp PRIVATE MatrixMath)
