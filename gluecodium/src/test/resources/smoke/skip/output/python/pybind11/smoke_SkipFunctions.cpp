

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SkipFunctions.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkipFunctions = ::smoke::SkipFunctions;


void register_SkipFunctions(py::module_& module) {
    py::class_<SkipFunctions, std::shared_ptr<SkipFunctions>>(module, "SkipFunctions")
        .def_static("not_in_java", &SkipFunctions::not_in_java, py::arg("input"))

        .def_static("not_in_swift", &SkipFunctions::not_in_swift, py::arg("input"))

        .def_static("not_in_dart", &SkipFunctions::not_in_dart, py::arg("input"))

        .def_static("not_in_kotlin", &SkipFunctions::not_in_kotlin, py::arg("input"))

        ;
}

