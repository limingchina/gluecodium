

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/NestedReferences.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NestedReferences = ::gluecodium::smoke::NestedReferences;

void register_NestedReferences(py::module_& module) {
    py::class_<NestedReferences, std::shared_ptr<NestedReferences>>(module, "NestedReferences")
        .def("inside_out", &NestedReferences::inside_out, py::arg("struct1"), py::arg("struct2"))
        ;
}

