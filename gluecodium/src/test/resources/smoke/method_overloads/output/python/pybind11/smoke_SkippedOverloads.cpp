

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkippedOverloads.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkippedOverloads = ::smoke::SkippedOverloads;

void register_SkippedOverloads(py::module_& module) {
    py::class_<SkippedOverloads, std::shared_ptr<SkippedOverloads>>(module, "SkippedOverloads")
        .def("make", &SkippedOverloads::make)
        .def("make_for_dart", &SkippedOverloads::make_for_dart, py::arg("input"))
        ;
}

