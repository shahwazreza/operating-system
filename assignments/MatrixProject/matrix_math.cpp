

#include "matrix_math.h"
#include <stdexcept>

std::vector<double> MatrixProcessor::addVectors(const std::vector<double>& a, const std::vector<double>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must be the same size.");
    }
    
    std::vector<double> result(a.size());
    for (size_t i = 0; i < a.size(); ++i) {
        result[i] = a[i] + b[i];
    }
    return result;
}

void MatrixProcessor::printVector(const std::vector<double>& vec) {
    std::cout << "[ ";
    for (double val : vec) {
        std::cout << val << " ";
    }
    std::cout << "]" << std::endl;
}

