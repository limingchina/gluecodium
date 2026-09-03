// Spike: confirm pybind11/chrono.h handles the exact C++ types the Gluecodium
// C++ generator emits for LIME Date / Duration:
//   Date     -> ::std::chrono::system_clock::time_point
//   Duration -> ::std::chrono::seconds   (NOTE: plan 4.1 said nanoseconds; the
//              actual CppNameResolver.kt:169 emits seconds)
#include <pybind11/chrono.h>
#include <pybind11/pybind11.h>
#include <chrono>

namespace py = pybind11;

using GluecodiumDate = std::chrono::system_clock::time_point;
using GluecodiumDuration = std::chrono::seconds;

GluecodiumDate get_epoch() {
    return std::chrono::system_clock::from_time_t(0);
}

GluecodiumDate add_days(GluecodiumDate d, int days) {
    return d + std::chrono::hours(24 * days);
}

GluecodiumDuration make_duration(int secs) {
    return std::chrono::seconds(secs);
}

GluecodiumDuration double_duration(GluecodiumDuration d) {
    return d * 2;
}

PYBIND11_MODULE(chrono_spike, m) {
    m.doc() = "Spike: Date/Duration via pybind11/chrono.h";
    m.def("get_epoch", &get_epoch);
    m.def("add_days", &add_days);
    m.def("make_duration", &make_duration);
    m.def("double_duration", &double_duration);
}
