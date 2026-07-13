

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipOverloadsInDart.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipOverloadsInDart = ::smoke::SkipOverloadsInDart;

void register_SkipOverloadsInDart(py::module_& module) {
    py::class_<SkipOverloadsInDart, std::shared_ptr<SkipOverloadsInDart>>(module, "SkipOverloadsInDart")
        .def("make", &SkipOverloadsInDart::make)
        .def("make", &SkipOverloadsInDart::make, py::arg("input"))
        ;
}

