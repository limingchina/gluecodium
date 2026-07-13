

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/NullableOverloads.h"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NullableOverloads = ::gluecodium::smoke::NullableOverloads;

void register_NullableOverloads(py::module_& module) {
    py::class_<NullableOverloads>(module, "NullableOverloads")
        .def("foo", &NullableOverloads::foo, py::arg("input"))
        .def("foo", &NullableOverloads::foo, py::arg("input"))
        ;
}

