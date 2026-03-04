#pragma once
#include <vector>
#include <iostream>

// Macro to handle DLL export/import on Windows
#ifdef _WIN32
  #ifdef BUILD_MATH_DLL
    #define MATH_API __declspec(dllexport)
  #else
    #define MATH_API __declspec(dllimport)
  #endif
#else
  #define MATH_API // Linux/macOS don't require this by default
#endif

// A simple class for vector operations
class MATH_API MatrixProcessor {
public:
    std::vector<double> addVectors(const std::vector<double>& a, const std::vector<double>& b);
    void printVector(const std::vector<double>& vec);
};
