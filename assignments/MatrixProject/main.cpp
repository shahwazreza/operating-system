#include <iostream>
#include <vector>
#include "matrix_math.h"

int main() {
    MatrixProcessor processor;

    std::vector<double> vec1 = {1.5, 2.0, 3.5};
    std::vector<double> vec2 = {0.5, 1.0, 1.5};

    std::cout << "Vector 1: ";
    processor.printVector(vec1);

    std::cout << "Vector 2: ";
    processor.printVector(vec2);

    try {
        std::vector<double> result = processor.addVectors(vec1, vec2);
        std::cout << "Result  : ";
        processor.printVector(result);
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
