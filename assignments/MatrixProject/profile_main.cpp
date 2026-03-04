

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <vector>

#include "matrix_math.h"

#ifdef _WIN32
  #define WIN32_LEAN_AND_MEAN
  #include <windows.h>
  #include <psapi.h>
#elif defined(__APPLE__)
  #include <mach/mach.h>
#else
  #include <unistd.h>
  #include <fstream>
#endif

static std::uint64_t get_rss_bytes() {
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS_EX pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc))) {
        return static_cast<std::uint64_t>(pmc.WorkingSetSize);
    }
    return 0;
#elif defined(__APPLE__)
    mach_task_basic_info info;
    mach_msg_type_number_t count = MACH_TASK_BASIC_INFO_COUNT;
    if (task_info(mach_task_self(), MACH_TASK_BASIC_INFO, (task_info_t)&info, &count) == KERN_SUCCESS) {
        return static_cast<std::uint64_t>(info.resident_size);
    }
    return 0;
else
    // Linux: read VmRSS from /proc/self/status
    std::ifstream status("/proc/self/status");
    std::string key;
    std::uint64_t value_kb = 0;
    while (status >> key) {
        if (key == "VmRSS:") {
            status >> value_kb; // in kB
            break;
        }
        // skip rest of the line
        status.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    return value_kb * 1024ULL;
#endif
}

static void print_human_bytes(std::uint64_t bytes) {
    const char* suffixes[] = {"B", "KB", "MB", "GB", "TB"};
    int i = 0;
    double count = static_cast<double>(bytes);
    while (count >= 1024.0 && i < 4) { count /= 1024.0; ++i; }
    std::cout << std::fixed << std::setprecision(2) << count << ' ' << suffixes[i];
}

int main(int argc, char** argv) {
    // Defaults
    std::size_t N = 10'000'000; // 10M elements ~= 76.3 MB for three vectors of doubles
    int iters = 5;

    // Very simple CLI parsing
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--size" && i + 1 < argc) {
            N = static_cast<std::size_t>(std::stoull(argv[++i]));
        } else if (arg == "--iters" && i + 1 < argc) {
            iters = std::stoi(argv[++i]);
        } else if (arg == "--help" || arg == "-h") {
            std::cout << "Usage: MatrixProfile [--size N] [--iters R]\n";
            return 0;
        }
    }

    std::cout << "Profiling addVectors on " << N << " doubles, " << iters << " iterations\n";

    // Prepare input data
    std::vector<double> a(N), b(N);
    for (std::size_t i = 0; i < N; ++i) {
        a[i] = static_cast<double>(i) * 0.5;
        b[i] = static_cast<double>(i) * 1.5;
    }

    MatrixProcessor proc;

    // Warm-up
    {
        auto r = proc.addVectors(a, b);
        (void)r;
    }

    auto rss_before = get_rss_bytes();

    std::vector<double> last_result;
    last_result.reserve(N);

    double best_ms = 1e300, sum_ms = 0.0;

    for (int it = 0; it < iters; ++it) {
        auto t0 = std::chrono::high_resolution_clock::now();
        auto r = proc.addVectors(a, b);
        auto t1 = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> ms = t1 - t0;
        best_ms = std::min(best_ms, ms.count());
        sum_ms += ms.count();
        last_result = std::move(r);
    }

    auto rss_after = get_rss_bytes();

    // Arithmetic intensity: reading 2*N doubles and writing N doubles
    const double bytes_moved = static_cast<double>(N) * 3.0 * sizeof(double);
    const double avg_ms = sum_ms / iters;

    std::cout << std::setprecision(3);
    std::cout << "Best time: " << best_ms << " ms\n";
    std::cout << "Avg  time: " << avg_ms  << " ms\n";
    std::cout << "Throughput (best): " << (bytes_moved / (best_ms / 1000.0)) / 1e9 << " GB/s\n";
    std::cout << "Throughput (avg) : " << (bytes_moved / (avg_ms  / 1000.0)) / 1e9 << " GB/s\n";

    std::cout << "RSS change: ";
    if (rss_after >= rss_before) {
        print_human_bytes(static_cast<std::uint64_t>(rss_after - rss_before));
        std::cout << " (from "; print_human_bytes(rss_before); std::cout << " to "; print_human_bytes(rss_after); std::cout << ")\n";
    } else {
        std::cout << "n/a\n";
    }

    // Sanity check on the last result
    if (!last_result.empty()) {
        std::cout << "Sample result values: [ " << last_result[0] << ", "
                  << last_result[N/2] << ", " << last_result.back() << " ]\n";
    }

    return 0;
}
