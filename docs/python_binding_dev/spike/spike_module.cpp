// pybind11 module exercising the Return<T, Error> caster spike.
#include <pybind11/pybind11.h>
#include <string>
#include <system_error>

#include "return_caster.h"
#include "return_spike.h"

namespace py = pybind11;

// --- Functions returning Return<T, std::error_code> ---
Return<int, std::error_code> divide(int a, int b) {
    if (b == 0) return std::make_error_code(std::errc::argument_list_too_long);
    return a / b;
}

Return<std::string, std::error_code> greet(const std::string& name) {
    if (name.empty()) return std::make_error_code(std::errc::invalid_argument);
    return "hello, " + name;
}

// --- Functions returning Return<T, custom error> ---
struct MyError {
    int code = 0;
    std::string message() const { return "MyError(" + std::to_string(code) + ")"; }
};

Return<double, MyError> sqrt_safe(double x) {
    if (x < 0.0) {
        MyError e;
        e.code = -1;
        return e;
    }
    return x * x;  // not really sqrt, just a demo value
}

PYBIND11_MODULE(spike_module, m) {
    m.doc() = "Spike: Return<T, Error> pybind11 type_caster";
    m.def("divide", &divide);
    m.def("greet", &greet);
    m.def("sqrt_safe", &sqrt_safe);
}
