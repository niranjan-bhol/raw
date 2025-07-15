#include <iostream>
#include <chrono>
#include <curl/curl.h>

size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    return size * nmemb;  // Discard response data
}

void send_request(const std::string& url) {
    CURL* curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 500); // Set timeout in milliseconds
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
}

int main() {
    const std::string url = "https://www.example.com";  // Change to your API endpoint // https://www.zerodha.com
    const int num_requests = 10;  // Number of requests to send

    auto start_time = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < num_requests; ++i) {
        send_request(url);
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end_time - start_time;

    std::cout << "Sent " << num_requests << " requests in " << duration.count() << " seconds\n";
    std::cout << "Average time per request: " << (duration.count() / num_requests) << " seconds\n";

    return 0;
}

/*
g++ -std=c++17 request_speed_test.cpp -o request_speed_test -lcurl
./request_speed_test
*/
