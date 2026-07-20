

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/off/NestedPackages.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NestedPackages = ::smoke::off::NestedPackages;


void register_NestedPackages(py::module_& module) {
    py::class_<NestedPackages, std::shared_ptr<NestedPackages>>(module, "NestedPackages")
        .def_static("basic_method", &NestedPackages::basic_method, py::arg("input"))

        ;
}

