

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/Currency.h"
#include "cstdint"
#include "string"

void register_Currency(py::module_& module) {
    py::class_<Currency>(module, "Currency")
        .def_readwrite("currency_code", &Currency::currency_code)
        .def_readwrite("numeric_code", &Currency::numeric_code)
        ;
}

