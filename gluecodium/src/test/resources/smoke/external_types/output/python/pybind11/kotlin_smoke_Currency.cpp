

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/Currency.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Currency = ::kotlin_smoke::Currency;

void register_kotlin_smoke_Currency(py::module_& module) {
    py::class_<Currency>(module, "Currency")
        .def_readonly("currency_code", &Currency::currency_code)
        .def_readonly("numeric_code", &Currency::numeric_code)
        .def(py::init<::std::string, int32_t(), py::arg("currency_code"), py::arg("numeric_code"))
        ;
}

