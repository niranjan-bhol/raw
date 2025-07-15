#include <iostream>
#include <chrono>

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    volatile long long result = 0;  // volatile prevents optimization
    for (long long i = 0; i < 1000000; i++) {
        result += i * i;  // Simple computation
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> execution_time = end - start;

    std::cout << "Execution Time: " << execution_time.count() << " seconds" << std::endl;
    return 0;
}

/*
g++ -std=c++17 measure_time.cpp -o measure_time
./measure_time
*/
