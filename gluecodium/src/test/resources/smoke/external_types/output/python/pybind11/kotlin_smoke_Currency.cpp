

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/Currency.h"
#include "cstdint"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Currency = ::gluecodium::kotlin_smoke::Currency;

void register_Currency(py::module_& module) {
    py::class_<Currency>(module, "Currency")
        .def_readwrite("currency_code", &Currency::currency_code)
        .def_readwrite("numeric_code", &Currency::numeric_code)
        ;
}

