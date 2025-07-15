#include <iostream>
#include <vector>
#include <future>
#include <chrono>
#include <cpr/cpr.h>

void send_request(const std::string& url, int id) {
    auto start = std::chrono::high_resolution_clock::now();
    cpr::Response r = cpr::Get(cpr::Url{url});  // Send GET request
    auto end = std::chrono::high_resolution_clock::now();
    
    std::chrono::duration<double, std::milli> duration = end - start;
    std::cout << "Request " << id << " completed in " << duration.count() << " ms, Status Code: " << r.status_code << "\n";
}

int main() {
    const std::string url = "https://www.example.com";  // Change to your test API
    const int N = 10;  // Number of requests

    auto start_all = std::chrono::high_resolution_clock::now();

    std::vector<std::future<void>> futures;
    for (int i = 0; i < N; i++) {
        futures.push_back(std::async(std::launch::async, send_request, url, i + 1));
    }

    for (auto& f : futures) {
        f.get();  // Wait for all requests to finish
    }

    auto end_all = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> total_duration = end_all - start_all;
    
    std::cout << "Total time for " << N << " asynchronous requests: " << total_duration.count() << " ms\n";

    return 0;
}

/*
brew install cpr

sudo apt install libcurl4-openssl-dev
git clone https://github.com/libcpr/cpr.git
cd cpr
mkdir build && cd build
cmake .. && make -j$(nproc)
sudo make install

sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo yum install cmake3 git curl-devel -y
sudo yum install openssl-devel -y
git clone https://github.com/libcpr/cpr.git
cd cpr
mkdir build && cd build
cmake3 .. -DCMAKE_BUILD_TYPE=Release -DCPR_USE_SYSTEM_CURL=ON
make -j$(nproc)
sudo make install

g++ -std=c++17 async_requests.cpp -o async_requests -lcpr -pthread
./async_requests

g++ -std=c++17 async_requests.cpp -o async_requests -lcpr -lcurl -lssl -lcrypto -pthread
./async_requests
*/
