

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SwiftConstructorOverloads.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SwiftConstructorOverloads = ::smoke::SwiftConstructorOverloads;

void register_SwiftConstructorOverloads(py::module_& module) {
    py::class_<SwiftConstructorOverloads, std::shared_ptr<SwiftConstructorOverloads>>(module, "SwiftConstructorOverloads")
        .def("make", &SwiftConstructorOverloads::make, py::arg("input"))
        .def("make_do", &SwiftConstructorOverloads::make_do, py::arg("throughput"))
        ;
}

